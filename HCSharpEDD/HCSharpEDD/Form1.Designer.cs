namespace HCSharpEDD
{
    partial class Form1
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
            pictureBox_display = new PictureBox();
            button_identify = new Button();
            label_time = new Label();
            label_time_ = new Label();
            ((System.ComponentModel.ISupportInitialize)pictureBox_display).BeginInit();
            SuspendLayout();
            // 
            // pictureBox_display
            // 
            pictureBox_display.Location = new Point(12, 12);
            pictureBox_display.Name = "pictureBox_display";
            pictureBox_display.Size = new Size(1298, 1031);
            pictureBox_display.TabIndex = 0;
            pictureBox_display.TabStop = false;
            // 
            // button_identify
            // 
            button_identify.Location = new Point(1333, 12);
            button_identify.Name = "button_identify";
            button_identify.Size = new Size(270, 32);
            button_identify.TabIndex = 1;
            button_identify.Text = "开始识别";
            button_identify.UseVisualStyleBackColor = true;
            button_identify.Click += button_identify_Click;
            // 
            // label_time
            // 
            label_time.AutoSize = true;
            label_time.Location = new Point(1333, 60);
            label_time.Name = "label_time";
            label_time.Size = new Size(68, 17);
            label_time.TabIndex = 2;
            label_time.Text = "运行时间：";
            // 
            // label_time_
            // 
            label_time_.AutoSize = true;
            label_time_.Location = new Point(86, 1029);
            label_time_.Name = "label_time_";
            label_time_.Size = new Size(0, 17);
            label_time_.TabIndex = 2;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 17F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1615, 1055);
            Controls.Add(label_time_);
            Controls.Add(label_time);
            Controls.Add(button_identify);
            Controls.Add(pictureBox_display);
            Name = "Form1";
            Text = "HCSharpEDD";
            ((System.ComponentModel.ISupportInitialize)pictureBox_display).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private PictureBox pictureBox_display;
        private Button button_identify;
        private Label label_time;
        private Label label_time_;
    }
}
