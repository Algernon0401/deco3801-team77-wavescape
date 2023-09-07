using System.Diagnostics;
using System.Net;
using System.Text;

namespace AppLauncher
{
    /// <summary>
    /// The loader form is the main interface of the launcher.
    /// It checks all dependencies of the app, prompts to launch python
    /// and installs any missing dependencies.
    /// </summary>
    public partial class LoaderForm : Form
    {
        public LoaderForm()
        {
            InitializeComponent();

            // Create a new thread to handle loading the app.
            _LoadingThread = new Thread(LaunchApp);
            _LoadingThread.Start();
            _LoadingThread.Priority = ThreadPriority.Lowest;
        }

        private Thread _LoadingThread;

        /// <summary>
        /// A function which occurs every tick of the animated opacity timer.
        /// Once Opacity reaches full, this timer is disposed and the function is never called again.
        /// </summary>
        /// <param name="sender">timer</param>
        /// <param name="e">event args</param>
        private void animatedOpacityTimer_Tick(object sender, EventArgs e)
        {
            // Update opacity
            if(Opacity<1)
            {
                double newOpacity = Opacity + 0.01;
                if(newOpacity>=1)
                {
                    newOpacity = 1; // Cap value to avoid error
                    // Timer is no longer need so dispose
                    animatedOpacityTimer.Dispose();
                }
                Opacity = newOpacity;
            }
        }

        /// <summary>
        /// The estimated progress of launching the app including dependencies check.
        /// </summary>
        private double _LoadingProgress = 0;

        private string _LoadingMessage = "Validating environment...";

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            try
            {
                // Abort the alternate thread if necessary.
                if (_LoadingThread.IsAlive)
                    _LoadingThread.Abort();
            }
            catch
            {

            }
            base.OnFormClosing(e);
        }

        private void crossthreadTimer_Tick(object sender, EventArgs e)
        {
            if(_LoadingProgress < 0)
            {
                // Crash the progress
                Dispose();
                return;
            }
            // Update progress bar percentage to loading thread progress.
            this.progressBar.Value = (int)(_LoadingProgress * 1000);

            // Update message to loading thread message.
            this.loadingMessage.Text = _LoadingMessage;

            if(_LoadingProgress >= 1)
            {
                // Destroy current form, ending the launcher's process.
                Dispose();
            }
        }

        #region Progress Steps
        public const double STEP_START = 0;
        public const double STEP_PYTHONINSTALLER = 0.2;
        public const double STEP_PYTHONVALID = 0.5;
        public const double STEP_DEPENDENCYSTART = 0.5;
        public const double STEP_DEPENDENCYEND = 0.9;
        public const double STEP_FINISHED = 1;
        #endregion
        /// <summary>
        /// Launches the app by checking the environment, checking any dependencies,
        /// and installing any missing dependencies.
        /// </summary>
        public async void LaunchApp()
        {
            // Fix directory to application
            Directory.SetCurrentDirectory(new FileInfo(Application.ExecutablePath).DirectoryName);

            #region Python Installation
            
            _LoadingProgress = STEP_START;
            _LoadingMessage = "Checking Python Installation...";

            string version = PythonHelper.GetVersion();

            if(version == null || !version.StartsWith("3"))
            {
                // Install python 3.11.5
                _LoadingMessage = "Downloading Python 3.11.5 (x64)";

                try
                {

                    // Download installer
                    Directory.CreateDirectory("tmp");

                    WebClient client = new WebClient();
                    client.DownloadFile(@"https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe", "tmp/python-3.11.5-amd64.exe");

                    _LoadingProgress = STEP_PYTHONINSTALLER;

                    // Install python
                    _LoadingMessage = "Installing Python 3.11.5 (x64)";
                    Process pythonInstaller = Process.Start(
                        "tmp/python-3.11.5-amd64.exe",
                        "InstallAllUsers=1 SimpleInstall=1 PrependPath=1 SimpleInstallDescription=\"Install Python.\""
                        );

                    pythonInstaller.WaitForExit();

                    // Check installation again

                    version = PythonHelper.GetVersion();

                    if (version == null || !version.StartsWith("3"))
                    {
                        // Crash launcher
                        MessageBox.Show(
                            "Failed to install python. The launcher will now crash.", "Python Error",
                            MessageBoxButtons.OK, MessageBoxIcon.Error
                            );
                        _LoadingProgress = -1;
                        return;
                    }
                } 
                catch (Exception exc)
                {
                    // Crash launcher
                    MessageBox.Show(
                        $"Failed to install python. A fatal error occurred: {exc.Message}", "Python Installation Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Error
                        );
                    _LoadingProgress = -1;
                    return;
                }
                Directory.Delete("tmp", true);
            }

            _LoadingProgress = STEP_PYTHONVALID;
            #endregion

            #region Check or Install Dependencies 
            _LoadingMessage = "Checking Python Dependencies...";
            if(File.Exists("dependencies.txt"))
            {
                string[] pipInstructions = File.ReadAllLines("dependencies.txt");
                string singleInstallations = ""; // e.g. pip install numpy pandas ...
                string singleInstallationNames = ""; // e.g. Numpy, Pandas, etc.
                List<(string, string)> complexInstallations = new List<(string, string)>(); // With -r requirements.txt
                foreach(string pipTarget in pipInstructions)
                {
                    // Ensure target is not empty.
                    // Each line should be in format
                    // name: package
                    // where package is the suffix of pip install.
                    string target = pipTarget.Trim();
                    if(target.Length > 0)
                    {
                        // Extract target name for debugging.
                        int colIndex = target.IndexOf(':');
                        if(colIndex == -1)
                        {
                            // Crash launcher
                            MessageBox.Show(
                                $"Dependencies list is invalid ('name: cmd' format not followed).", "Dependency Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error
                                );
                            _LoadingProgress = -1;
                            return;
                        }

                        // Extract name and cmd from name:cmd
                        string name = target.Substring(0, colIndex).Trim();
                        string cmd = target.Substring(colIndex + 1).Trim();

                        if(cmd.StartsWith("-r"))
                        {
                            complexInstallations.Add((name, cmd));
                        }
                        else
                        {
                            if (singleInstallations.Length != 0)
                            {
                                singleInstallations += " "; // Indicates new package
                                singleInstallationNames += " ";
                            }
                            singleInstallations += cmd;
                            singleInstallationNames += name;
                        }
                    }
                }

                try
                {
                    // Create log file for reference
                    FileStream log = File.Create("install.log");

                    if (singleInstallations.Length > 0)
                    {
                        // Install/check chained single installations
                        log.Write(Encoding.UTF8.GetBytes($"Installing {singleInstallationNames}...\n"));

                        PythonHelper.RunPip(singleInstallations, (data) =>
                        {
                            if (data == null) data = "";
                            else _LoadingMessage = data;
                            log.Write(Encoding.UTF8.GetBytes(data+"\n"));
                        });
                    }

                    foreach((string name, string cmd) in complexInstallations)
                    {
                        log.Write(Encoding.UTF8.GetBytes($"\nInstalling {name}...\n"));
                        
                        PythonHelper.RunPip(cmd, (data) =>
                        {
                            if (data == null) data = "";
                            else _LoadingMessage = data;
                            log.Write(Encoding.UTF8.GetBytes(data + "\n"));
                        });
                    }
                    
                    // Flush and dispose log file to write
                    log.Flush();
                    log.Dispose();
                }
                catch (Exception exc)
                {
                    // Crash launcher
                    MessageBox.Show(
                        $"Failed to check/install dependencies. A fatal error occurred: {exc.Message}", "Python Dependency Installation Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Error
                        );
                    _LoadingProgress = -1;
                    return;
                }
            }
            #endregion

            _LoadingProgress = STEP_DEPENDENCYEND;
            _LoadingMessage = "Launching app.py...";
            #region Launch App.py
            if (version != null)
            {
                // Can now launch app.py, which should be in the local directory.
                if(!File.Exists("app.py"))
                {
                    // Crash launcher
                    MessageBox.Show(
                        $"Failed to launch app, as app.py does not exist.", "Python App Launch Error",
                        MessageBoxButtons.OK, MessageBoxIcon.Error
                        );
                    _LoadingProgress = -1;
                    return;
                }
                PythonHelper.RunFile("app.py");
            }
            _LoadingProgress = STEP_FINISHED;
            #endregion
        }

        private void launcherProcess_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            
        }
    }
}