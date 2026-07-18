using System;

namespace SmartAgriculture.Models
{
    public class SensorData
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public float Temperature { get; set; }
        public float Humidity { get; set; }
        public int Light { get; set; }
        public int CO2 { get; set; }
        public float Pressure { get; set; }
        public bool FanOn { get; set; }
        public bool LightOn { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
