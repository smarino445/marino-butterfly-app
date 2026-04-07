import base64
import requests
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# Clean + Responsive Streamlit OIDC Starter + CNN Endpoint Prediction
# - White background, sans-serif font stack (incl. Helvetica Neue)
# - Tabs: Login | Butterfly Prediction
# - OIDC gate: prediction only available after login
# - Upload or camera image -> base64 -> POST to endpoint -> show predicted_label
# ──────────────────────────────────────────────────────────────────────────────

# Change ONLY if your endpoint changes
ENDPOINT_URL = "https://askai.aiclub.world/83845c7c-6fc6-42c0-a3d4-b1918a688783"

st.set_page_config(page_title="Butterfly Classifier (OIDC)", layout="centered")

# ----------------------------- ACCESSIBILITY CONTROLS --------------------------
with st.sidebar:
    st.markdown("### Accessibility")
    base_size = st.slider("Base text size", 14, 24, 16, help="Increase for readability")
    high_contrast = st.toggle("High contrast mode", value=False)
    dyslexia_font = st.toggle("Dyslexia-friendly font (fallback)", value=False)
    reduce_motion = st.toggle("Reduce motion", value=False)
    underline_links = st.toggle("Underline links", value=True)
    widen_layout = st.toggle("Wider reading layout", value=False)
    show_helper_text = st.toggle("Show helper text", value=True)

    # Optional toggles you can demo with teachers
    increase_line_height = st.toggle("Increase line spacing", value=False)
    reduce_shadows = st.toggle("Reduce shadows", value=False)

# ----------------------------- GLOBAL CSS (RESPONSIVE) -------------------------
font_stack = (
    '"Helvetica Neue", Helvetica, Arial, system-ui, -apple-system, Segoe UI, Roboto, sans-serif'
)
dyslexia_stack = (
    '"OpenDyslexic", "Atkinson Hyperlegible", "Lexend", '
    '"Helvetica Neue", Helvetica, Arial, system-ui, -apple-system, Segoe UI, Roboto, sans-serif'
)

BASE_CSS = f"""
<style>
:root {{
  --bg: #ffffff;
  --surface: #ffffff;
  --text: #111827;
  --muted: #4b5563;
  --border: #e5e7eb;
  --brand: #2563eb;
  --brandHover: #1d4ed8;
  --focus: #f59e0b;
  --radius: 14px;
  --shadow: {"0 6px 24px rgba(17, 24, 39, 0.08)" if not reduce_shadows else "none"};
  --maxw: {1150 if widen_layout else 900}px;
  --font: {font_stack};
  --font-dys: {dyslexia_stack};
  --lineh: {1.7 if increase_line_height else 1.45};
}}

html {{
  font-size: {base_size}px;
}}

body, [data-testid="stAppViewContainer"] {{
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  line-height: var(--lineh) !important;
}}

a, .stMarkdown a {{
  color: var(--brand) !important;
  text-decoration: {"underline" if underline_links else "none"} !important;
  text-underline-offset: 2px;
}}
a:hover, .stMarkdown a:hover {{ color: var(--brandHover) !important; }}

h1, h2, h3, h4, h5, h6 {{
  color: var(--text) !important;
  letter-spacing: -0.01em;
}}

[data-testid="stSidebar"] > div:first-child {{
  background: #f9fafb !important;
  border-right: 1px solid var(--border);
}}

*:focus {{
  outline: 3px solid var(--focus) !important;
  outline-offset: 2px !important;
  border-radius: 6px;
}}

{"@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; scroll-behavior:auto !important; } }" if reduce_motion else ""}

.block-container {{
  padding-top: 1.25rem !important;
  padding-bottom: 2.5rem !important;
  max-width: var(--maxw);
}}

@media (max-width: 640px) {{
  .block-container {{
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
  }}
}}

.card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.0rem;
}}

.card + .card {{
  margin-top: 1rem;
}}

.stButton > button {{
  border-radius: 12px !important;
  padding: 0.65rem 0.9rem !important;
  font-weight: 600 !important;
}}

[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {{
  border-radius: 12px !important;
}}

{"body * { font-family: var(--font-dys) !important; }" if dyslexia_font else ""}

/* High contrast mode */
{" :root { --text:#000000; --muted:#111827; --border:#111827; --brand:#0000EE; --brandHover:#0000AA; } " if high_contrast else ""}
</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)

def card_open():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def safe_user_field(*keys: str):
    """Try multiple keys from st.user and return the first non-empty value."""
    try:
        u = st.user
    except Exception:
        return None
    for k in keys:
        try:
            v = u.get(k)
            if v:
                return v
        except Exception:
            pass
    return None

def show_oidc_setup_check():
    """Non-sensitive OIDC sanity check for deployments."""
    with st.sidebar.expander("OIDC setup check"):
        auth_cfg = dict(st.secrets.get("auth", {})) if hasattr(st, "secrets") else {}
        st.write(
            {
                "redirect_uri": auth_cfg.get("redirect_uri", "(missing)"),
                "server_metadata_url": auth_cfg.get("server_metadata_url", "(missing)"),
                "client_id_present": bool(auth_cfg.get("client_id")),
                "cookie_secret_present": bool(auth_cfg.get("cookie_secret")),
            }
        )
        if show_helper_text:
            st.caption("Redirect URI must match Google OAuth Authorized redirect URI exactly.")

# ----------------------------- PREDICTION HELPERS ------------------------------
ALLOWED_EXT = {"jpg", "jpeg", "png", "jfif"}

def call_model_endpoint(image_bytes: bytes, url: str) -> str:
    """
    Base64-encode image bytes and POST to the model endpoint.
    Returns predicted_label if present.
    """
    payload_b64 = base64.b64encode(image_bytes)

    try:
        # NOTE: your endpoint expects base64 bytes in the request body (data=...).
        r = requests.post(url, data=payload_b64, timeout=30)
        r.raise_for_status()
        js = r.json()
        return js.get("predicted_label", "Unknown")
    except requests.exceptions.Timeout:
        st.error("Prediction timed out. Please try again.")
        return "Error"
    except Exception as e:
        st.error(f"Prediction request failed: {e}")
        return "Error"

# ----------------------------- UI: HEADER + TABS -------------------------------
st.markdown("# Butterfly App")
st.caption("A responsive Streamlit example for mobile, tablet, laptop, and desktop.")

tabs = st.tabs(["Login", "Butterfly Prediction"])

# ----------------------------- TAB: LOGIN -------------------------------------
with tabs[0]:
    card_open()
    st.markdown("## Login")
    st.write("Sign in with Google to capture your **name** and **email address** for personalization.")
    card_close()

    card_open()
    if not st.user.is_logged_in:
        st.write("Status: **Not signed in**")
        if st.button("Log in with Google", type="primary"):
            st.login()
        show_oidc_setup_check()
    else:
        display_name = safe_user_field("name", "full_name", "display_name") or "Signed-in user"
        email = safe_user_field("email")

        st.write("Status: **Signed in** ✅")
        st.write({"name": display_name, "email": email})

        if st.button("Log out", type="secondary"):
            st.logout()
    card_close()

# ----------------------------- TAB: BUTTERFLY PREDICTION -----------------------
with tabs[1]:
    if not st.user.is_logged_in:
        card_open()
        st.warning("Please log in first (use the **Login** tab).")
        card_close()
        st.stop()

    display_name = safe_user_field("name", "full_name", "display_name") or "Signed-in user"
    email = safe_user_field("email")

    HERO_URL = (
        "https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0"
    )
    HERO_DESC = "Monarch butterfly on a flower (decorative background for the classifier)."

    card_open()
    st.markdown(f"## Butterfly Classifier")
    st.caption(f"Signed in as: {display_name}" + (f" • {email}" if email else ""))

    st.image(HERO_URL, caption="Butterfly classification background image", use_container_width=True)
    st.caption(f"Image description: {HERO_DESC}")
    card_close()

    card_open()
    st.markdown("### Upload or capture a butterfly image")
    st.caption("Then click **Predict** to query the model endpoint.")

    sub_tabs = st.tabs(["Image Upload", "Camera Upload"])

    # -------- Image Upload --------
    with sub_tabs[0]:
        image = st.file_uploader(
            label="Upload a butterfly image",
            accept_multiple_files=False,
            type=list(ALLOWED_EXT),
            help="Supported: jpg, jpeg, png, jfif",
        )

        if image:
            # Optional: validate MIME extension
            ext = (image.type.split("/")[-1] or "").lower()
            if ext not in ALLOWED_EXT:
                st.error(f"Invalid file type: {image.type}")
            else:
                st.image(image, caption="Uploaded image", use_container_width=True)

                if st.button("Predict (Upload)", type="primary"):
                    label = call_model_endpoint(image.getvalue(), ENDPOINT_URL)
                    if label not in {"Error", "Unknown"}:
                        st.success(f"Class Label: **{label}**")
                    elif label == "Unknown":
                        st.warning("Prediction returned 'Unknown'.")
                    else:
                        st.error("Could not retrieve a valid prediction.")

    # -------- Camera Upload --------
    with sub_tabs[1]:
        cam_image = st.camera_input("Take a photo")
        if cam_image:
            st.image(cam_image, caption="Captured image", use_container_width=True)

            if st.button("Predict (Camera)", type="primary"):
                label = call_model_endpoint(cam_image.getvalue(), ENDPOINT_URL)
                if label not in {"Error", "Unknown"}:
                    st.success(f"Class Label: **{label}**")
                elif label == "Unknown":
                    st.warning("Prediction returned 'Unknown'.")
                else:
                    st.error("Could not retrieve a valid prediction.")

    card_close()
