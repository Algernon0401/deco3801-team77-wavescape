using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Win32;

namespace AppLauncher
{
    /// <summary>
    /// Contains methods for checking python and dependencies, and installing dependencies.
    /// </summary>
    public static class PythonHelper
    {
        /// <summary>
        /// Gets the highest version of python that is currently installed on this computer.
        /// </summary>
        /// <returns>null if no python installation exists, else the version</returns>
        public static string GetVersion()
        {
            // Check python key that exists in HKEY_CURRENT_USER\Software\Python\PythonCore
            // or in KEY_CURRENT_USER\Software\Python\PythonCore
            RegistryKey core = Registry.LocalMachine.OpenSubKey(@"Software\Python\PythonCore");
            if (core == null) core = Registry.CurrentUser.OpenSubKey(@"Software\Python\PythonCore");
            if (core == null) return null;
            
            // Get python versions and sort by name (2 < 3)
            List<string> subkeys = core.GetSubKeyNames().ToList();
            subkeys.Sort();

            core.Close();

            if(subkeys.Count > 0)
            {
                return subkeys.Last(); // Last is highest version of path.
            }
            return null;
        }
        /// <summary>
        /// Gets the path of highest version of python that is currently installed on this computer.
        /// </summary>
        /// <returns>null if no python installation exists, else of the </returns>
        public static string GetPythonPath()
        {
            // Check python key that exists in HKEY_CURRENT_USER\Software\Python\PythonCore
            // or in KEY_CURRENT_USER\Software\Python\PythonCore
            try
            {
                RegistryKey core = Registry.LocalMachine.OpenSubKey(@"Software\Python\PythonCore");
                if (core == null) core = Registry.CurrentUser.OpenSubKey(@"Software\Python\PythonCore");
                if (core == null) return "python"; // Default to python PATH

                // Get python versions and sort by name (2 < 3)
                List<string> subkeys = core.GetSubKeyNames().ToList();
                subkeys.Sort();

                if (subkeys.Count > 0)
                {
                    // Get install path, which has a key of executable path
                    RegistryKey installPath = core.OpenSubKey($"{subkeys.Last()}\\InstallPath");
                    if (installPath != null)
                    {
                        string path = installPath.GetValue("ExecutablePath") as string;
                        core.Close();
                        installPath.Close();
                        return path;
                    }
                }
                core.Close();
            }
            catch (Exception exc) { try { File.WriteAllText("python.error", "Could not find python registry path"); } catch { } }
            return "python"; // Default to python PATH
        }

        /// <summary>
        /// Checks and installs the given packages using the pip installer.
        /// </summary>
        /// <param name="file">the python file to run</param>
        /// <returns>the process of python running the app</returns>
        public static Process RunFile(string file)
        {
            // Create start info for pip
            ProcessStartInfo fileRunCommandInfo = new ProcessStartInfo(
                        GetPythonPath(),
                        file
                        );
            fileRunCommandInfo.UseShellExecute = false;
            fileRunCommandInfo.RedirectStandardOutput = true;
            fileRunCommandInfo.WindowStyle = ProcessWindowStyle.Hidden;
            fileRunCommandInfo.CreateNoWindow = true;

            // Run app dependencies
            Process pythonRunProcess = new Process();
            pythonRunProcess.StartInfo = fileRunCommandInfo;
            pythonRunProcess.Start();

            return pythonRunProcess;
        }


        /// <summary>
        /// The function which outputs the realtime output lines of the pip process.
        /// </summary>
        private static Action<string> RealtimePipOutputFunction;
        /// <summary>
        /// Checks and installs the given packages using the pip installer.
        /// </summary>
        /// <param name="packageSuffix">the suffix of the pip install command</param>
        /// <param name="realtimeOutput">a function which handles real-time output from pip</param>
        public static void RunPip(string packageSuffix, Action<string> realtimeOutput=null)
        {
            // Create start info for pip
            ProcessStartInfo pipSingleInstallInfo = new ProcessStartInfo(
                        GetPythonPath(),
                        "-m pip install " + packageSuffix
                        );
            pipSingleInstallInfo.UseShellExecute = false;
            pipSingleInstallInfo.RedirectStandardOutput = true;
            pipSingleInstallInfo.WindowStyle = ProcessWindowStyle.Hidden;
            pipSingleInstallInfo.CreateNoWindow = true;

            // Install/check dependencies
            Process pipInstall = new Process();
            pipInstall.StartInfo = pipSingleInstallInfo;
            pipInstall.OutputDataReceived += PipInstall_OutputDataReceived;
            RealtimePipOutputFunction = realtimeOutput;
            pipInstall.Start();
            pipInstall.BeginOutputReadLine();
            pipInstall.WaitForExit();
        }

        private static void PipInstall_OutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            // Use function to handle string.
            if (RealtimePipOutputFunction != null)
                RealtimePipOutputFunction(e.Data);
        }
    }
}
