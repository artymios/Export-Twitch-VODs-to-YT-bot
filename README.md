## A video explaining the process will be included soon

## Instructions

1. **Install a Code Editor**
    - Download and install a code editor of your choice, such as [Visual Studio Code](https://code.visualstudio.com/).

2. **Download the Project Files**
    - Download the zip file of this project from the repository.
    - Unpack the zip file to a directory of your choice.

3. **Download Chrome Version 114 (yes, it needs to be this version specifically)**
    > **Warning:** Be cautious of websites that may attempt to download harmful software. Ensure you download software from trusted sources.
    - For more information, you can refer to [Chrome for Testing](https://developer.chrome.com/blog/chrome-for-testing).

4. **Set Up Twitch on Chrome**
    - Open Chrome and log in to your Twitch account.
    - Make sure your YouTube account is connected to your Twitch account and you have the "Export" option available in the Video Producer.
    - Make sure Chrome is closed before running the script and that there are **NO TWITCH EXTENSIONS** enabled as that will cause the script not to work.

5. **Install Python**
    - Install Python via pip by running the command
        ```sh
        pip install python
        ```
    or from the [Microsoft Store](https://apps.microsoft.com/detail/9PNRBTZXMB4Z).

6. **Install Selenium**
    - Open your terminal or command prompt (VS Code -> Ctrl+Shift+') and run the following command:
      ```sh
      pip install selenium
      ```

7. **Edit lines 14-18**
    - The program requires some information where the Chrome installation file is, as well as what your Twitch username is.
  
8. **Run the program**
    - Enter the command below into the terminal and answer the questions with a y or an n. The script will use the same preferences if you run it again.
      ```sh
      python main.py
      ```
