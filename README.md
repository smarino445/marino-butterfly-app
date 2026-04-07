Yes — **you are absolutely right**.
**Step 5 (replacing your AIClub endpoint URL) should happen *before* deploying to Streamlit.**

This prevents:

* accidental use of **your** model,
* confusing prediction errors,
* unnecessary redeploys.

Below is a **cleanly rewritten README** with the **correct order**, explicit **GitHub edit/commit instructions**, and no ambiguity for students.

You can **replace your README.md entirely** with the version below.

---

# 🦋 Streamlit Butterfly App — Google OIDC + AI Model Starter (Template)

**Instructor:** Dr. Mistretta
**Course Context:** Master’s-level educators learning to *vibe code* and deploy responsive, accessible Streamlit applications using GitHub, Streamlit Community Cloud, Google OIDC, and external AI models.

This repository is a **GitHub Template Repository**.

🚫 **Do NOT fork this repository**
✅ Use **“Use this template”** to create your own independent Streamlit app.

---

## 🎯 What this starter app demonstrates

* A **clean, responsive Streamlit UI** for:

  * mobile phones
  * tablets
  * laptops
  * desktop computers
* **Google OpenID Connect (OIDC)** login using:

  * `st.login()`
  * `st.logout()`
  * `st.user` (captures name + email)
* A **tab-based layout**:

  * Login
  * Butterfly Prediction
* **Accessibility-forward design**, including:

  * adjustable text size
  * high-contrast mode
  * dyslexia-friendly font option
  * reduced-motion support
* Integration with an **external CNN image-classification model**
* A professional **starter-template workflow** used in industry

---

## 🚀 Student Instructions (Follow in Order)

---

## Step 1 — Create your own repository from this template

1. Go to:
   👉 [https://github.com/drmistretta/streamlit-butterfly-oidc-template](https://github.com/drmistretta/streamlit-butterfly-oidc-template)
2. Click **Use this template**.
3. Choose **Create a new repository**.
4. Name your repository (example):

   ```
   lastname-butterfly-app
   ```
5. Click **Create repository from template**.

✅ You now have your **own repository**.

---

## 🧠 Step 2 — REQUIRED: Replace the AI model endpoint URL (before deploying)

🚫 **You may NOT use Dr. Mistretta’s AIClub model URL.**
Each student must connect the app to **their own trained model**.

### 2.1 Open `app.py` in GitHub

1. In your new repository, click **app.py**
2. Click the **pencil icon (✏️ Edit)**

---

### 2.2 Replace the AI model endpoint URL

Near the top of the file, find this line:

```python
ENDPOINT_URL = "https://askai.aiclub.world/XXXXXX"
```

Replace it with **your own AIClub model endpoint**, for example:

```python
ENDPOINT_URL = "https://askai.aiclub.world/YOUR-UNIQUE-MODEL-ID"
```

⚠️ If you do not replace this URL, predictions will fail or violate course expectations.

---

### 2.3 Commit your changes

1. Scroll to the bottom of the page
2. In **Commit changes**:

   * Commit directly to `main`
   * Commit message example:

     ```
     Replace AI model endpoint URL
     ```
3. Click **Commit changes**

✅ Your app is now correctly configured for *your* model.

---

## ☁️ Step 3 — Deploy your app on Streamlit Community Cloud

Now that your code is correct, deploy the app.

1. Go to **Streamlit Community Cloud**
2. Click **Deploy app**
3. Select:

   * **Repository:** your new repo
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Click **Deploy**

After deployment, copy your app URL. It will look like:

```
https://your-app-name.streamlit.app
```

You will need this URL for Google login setup.

---

## 🔐 Step 4 — Create Google OAuth credentials (console.google.com)

Each student must complete this step **individually**.

---

### 4.1 Open Google Cloud Console

1. Go to 👉 [https://console.google.com](https://console.google.com)
2. Sign in with your Google account

---

### 4.2 Create or select a project

1. Click the **project dropdown** (top left)
2. Click **New Project**
3. Project name example:

   ```
   Butterfly Streamlit App
   ```
4. Click **Create**
5. Ensure your project is selected

---

### 4.3 Configure OAuth consent screen

1. Go to:

   ```
   APIs & Services → OAuth consent screen
   ```
2. Choose **External**
3. Click **Create**
4. Fill in:

   * App name
   * User support email
   * Developer contact email
5. Click **Save and Continue** through all steps

---

### 4.4 Create OAuth Client ID

1. Go to:

   ```
   APIs & Services → Credentials
   ```
2. Click **Create Credentials → OAuth client ID**
3. Application type: **Web application**
4. Name example:

   ```
   Streamlit Butterfly App
   ```

---

### 4.5 Add Authorized Redirect URI (VERY IMPORTANT)

Add this **exact** URI:

```
https://your-app-name.streamlit.app/oauth2callback
```

⚠️ Must match **exactly**:

* `https`
* your full Streamlit app name
* single `/oauth2callback`
* no trailing slash

Click **Create**, then copy:

* **Client ID**
* **Client Secret**

---

## 🔒 Step 5 — Add secrets to Streamlit (do NOT commit these)

1. Open your app in **Streamlit Community Cloud**
2. Go to **Settings → Secrets**
3. Paste:

```toml
[auth]
redirect_uri = "https://your-app-name.streamlit.app/oauth2callback"
cookie_secret = "generate-a-long-random-string"
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

4. Click **Save**
5. Wait for the app to restart

---

## ✅ Step 6 — Test your app

1. Open your Streamlit app URL
2. Go to the **Login** tab
3. Click **Log in with Google**
4. Confirm:

   * your name appears
   * your email appears
5. Go to **Butterfly Prediction**
6. Upload or capture an image
7. Click **Predict**

🎉 Your app is now live, authenticated, and connected to **your own AI model**.

---

## 📁 Repository contents

```
app.py                  # Main Streamlit app
requirements.txt        # streamlit[auth], requests
.gitignore              # Protects secrets
README.md               # This file
.streamlit/config.toml  # Optional Streamlit config
```

---

## ⚠️ Common Issues

### redirect_uri_mismatch

* Redirect URI in Google Console does not exactly match Streamlit URL

### Prediction fails

* You forgot to replace the AI model endpoint URL
* Your model endpoint is inactive or private

---

## ✅ License

No license is applied to this repository for instructional use.

---


