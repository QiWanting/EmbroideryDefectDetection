using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using System.Drawing.Imaging;
using Yolov5Net.Scorer;
using Yolov5Net.Scorer.Models;

namespace HCSharpEDD
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private string pictureFilePath =
            "D:\\own\\2024\\tian\\yolov8quexianjiance\\Code\\EmbroideryDefectDetection\\HCSharpEDD\\Data\\cat.14.jpg";
        private string onnxFilePath =
            "D:\\own\\2024\\tian\\yolov8quexianjiance\\Code\\EmbroideryDefectDetection\\HCSharpEDD\\Data\\Weights\\best.onnx";

        private void button_identify_Click(object sender, EventArgs e)
        {
            var image = System.Drawing.Image.FromFile(pictureFilePath);
            Image<Rgba32> outputImage;
            #region 将bitmap类型转换成Image<Rgba32>
            using (var inputImage = System.Drawing.Image.FromFile(pictureFilePath))
            {
                using (var memoryStream = new MemoryStream())
                {
                    inputImage.Save(memoryStream, ImageFormat.Png);
                    memoryStream.Position = 0;
                    outputImage = SixLabors.ImageSharp.Image.Load<Rgba32>(memoryStream);
                }
            }
            #endregion

            #region 识别并框出物体
            DateTime T_start = DateTime.Now;
            var scorer = new YoloScorer<YoloCocoP5Model>(onnxFilePath);
            List<YoloPrediction> predictions = scorer.Predict(outputImage);
            var graphics = Graphics.FromImage(image);
            foreach (var prediction in predictions)
            {
                double score = Math.Round(prediction.Score, 2);

                SixLabors.ImageSharp.RectangleF rectangleRange = prediction.Rectangle;
                System.Drawing.RectangleF rectangle = new System.Drawing.RectangleF(
                    rectangleRange.X, rectangleRange.Y, rectangleRange.Width, rectangleRange.Height);
                graphics.DrawRectangles(new System.Drawing.Pen(System.Drawing.Color.Red, 1),
                new[] { rectangle });
                var (x, y) = (prediction.Rectangle.X - 3, prediction.Rectangle.Y - 23);

                graphics.DrawString($"{prediction.Label.Name} ({score})",
                    new Font("Consolas", 16, GraphicsUnit.Pixel), new SolidBrush(System.Drawing.Color.Red),
                    new System.Drawing.PointF(x, y));
            }
            image.Save("result.jpg");
            this.pictureBox_display.Image = image;
            DateTime T_end = DateTime.Now;
            #endregion

            TimeSpan T_esp = T_end - T_start;
            this.label_time_.Text = T_esp.TotalMilliseconds.ToString();
        }
    }
}
