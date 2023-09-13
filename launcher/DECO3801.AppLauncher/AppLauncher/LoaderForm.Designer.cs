namespace AppLauncher
{
    partial class LoaderForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.mainContainer = new System.Windows.Forms.Panel();
            this.progressBar = new System.Windows.Forms.ProgressBar();
            this.loadingMessage = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.animatedOpacityTimer = new System.Windows.Forms.Timer(this.components);
            this.crossthreadTimer = new System.Windows.Forms.Timer(this.components);
            this.mainContainer.SuspendLayout();
            this.SuspendLayout();
            // 
            // mainContainer
            // 
            this.mainContainer.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.mainContainer.Controls.Add(this.progressBar);
            this.mainContainer.Controls.Add(this.loadingMessage);
            this.mainContainer.Controls.Add(this.label2);
            this.mainContainer.Controls.Add(this.label1);
            this.mainContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.mainContainer.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.mainContainer.Location = new System.Drawing.Point(0, 0);
            this.mainContainer.Name = "mainContainer";
            this.mainContainer.Size = new System.Drawing.Size(494, 168);
            this.mainContainer.TabIndex = 0;
            // 
            // progressBar
            // 
            this.progressBar.Location = new System.Drawing.Point(11, 84);
            this.progressBar.Maximum = 1000;
            this.progressBar.Name = "progressBar";
            this.progressBar.Size = new System.Drawing.Size(470, 23);
            this.progressBar.TabIndex = 3;
            // 
            // loadingMessage
            // 
            this.loadingMessage.Font = new System.Drawing.Font("Segoe UI", 8.25F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point);
            this.loadingMessage.Location = new System.Drawing.Point(11, 110);
            this.loadingMessage.Name = "loadingMessage";
            this.loadingMessage.Size = new System.Drawing.Size(470, 48);
            this.loadingMessage.TabIndex = 2;
            this.loadingMessage.Text = "Validating Environment...";
            this.loadingMessage.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label2
            // 
            this.label2.Font = new System.Drawing.Font("Segoe UI Semibold", 21.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point);
            this.label2.Location = new System.Drawing.Point(11, 8);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(470, 39);
            this.label2.TabIndex = 1;
            this.label2.Text = "DECO3801 Python App Launcher";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // label1
            // 
            this.label1.Font = new System.Drawing.Font("Segoe UI", 8.25F, System.Drawing.FontStyle.Italic, System.Drawing.GraphicsUnit.Point);
            this.label1.Location = new System.Drawing.Point(11, 47);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(470, 23);
            this.label1.TabIndex = 0;
            this.label1.Text = "Brought to you by Team \"{{7*7}}\"";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // animatedOpacityTimer
            // 
            this.animatedOpacityTimer.Enabled = true;
            this.animatedOpacityTimer.Interval = 10;
            this.animatedOpacityTimer.Tick += new System.EventHandler(this.animatedOpacityTimer_Tick);
            // 
            // crossthreadTimer
            // 
            this.crossthreadTimer.Enabled = true;
            this.crossthreadTimer.Interval = 30;
            this.crossthreadTimer.Tick += new System.EventHandler(this.crossthreadTimer_Tick);
            // 
            // LoaderForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(494, 168);
            this.Controls.Add(this.mainContainer);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "LoaderForm";
            this.Opacity = 0D;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "DECO3801 App Loader";
            this.mainContainer.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private Panel mainContainer;
        private Label label2;
        private Label label1;
        private Label loadingMessage;
        private ProgressBar progressBar;
        private System.Windows.Forms.Timer animatedOpacityTimer;
        private System.Windows.Forms.Timer crossthreadTimer;
    }
}