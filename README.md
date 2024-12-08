### Instruction Manual

# Setting up your Groq API key

To use the application, you need to set up an environment variable to securely store your Groq API key. Follow the instructions below for your operating system.

---

## Step 1: Obtain Your Groq API Key
1. Visit the [Groq API dashboard](https://groq.ai) (or your designated provider's site).
2. Log in to your account.
3. Navigate to the API settings and generate an API key.
4. Copy the API key.

---

## Step 2: Set Up the Environment Variable
### For Windows:
1. **Open the Environment Variables Dialog:**
   - Press `Win + S` and type **Environment Variables**.
   - Click on **Edit the system environment variables**.
   - In the dialog that opens, click the **Environment Variables** button.

2. **Add a New User Variable:**
   - Under **User variables**, click **New**.
   - For **Variable Name**, enter:
     ```
     GROQ_API_KEY
     ```
   - For **Variable Value**, paste your Groq API key.
   - Click **OK** to save.

3. **Close and Restart:**
   - Close all dialog boxes.
   - Restart your terminal or development environment to ensure the variable is loaded.

---

### For macOS/Linux:
1. **Edit Your Shell Configuration File:**
   - Open a terminal.
   - Based on your shell, edit the appropriate file:
     - For `bash`, use `~/.bashrc` or `~/.bash_profile`.
     - For `zsh`, use `~/.zshrc`.

2. **Add the Environment Variable:**
   - Add the following line at the end of the file:
     ```bash
     export GROQ_API_KEY="your_api_key_here"
     ```
   - Replace `your_api_key_here` with your actual Groq API key.

3. **Apply the Changes:**
   - Run the following command to apply the changes immediately:
     ```bash
     source ~/.bashrc  # or ~/.zshrc
     ```

---

## Step 3: Verify the Environment Variable
1. Open a terminal and type:
   ```bash
   echo $GROQ_API_KEY  # For macOS/Linux
   ```
   Or for Windows:
   ```cmd
   echo %GROQ_API_KEY%
   ```
2. You should see your API key printed. If it’s not showing, revisit the setup steps.

---

## Step 4: Run the Application
Once the environment variable is set up, you’re ready to use the application. The program will automatically retrieve your API key from the environment and authenticate with Groq.

---

**Note:** Never hard-code your API key into your scripts or share it publicly. Using environment variables keeps your credentials secure and manageable.
