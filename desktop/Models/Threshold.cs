namespace SmartAgriculture.Models
{
    /// <summary>In-memory display thresholds; they are never sent to a device.</summary>
    public class Threshold
    {
        public float TempMax { get; set; } = 35f;
        public float TempMin { get; set; } = 10f;
        public float HumidityMax { get; set; } = 80f;
        public float HumidityMin { get; set; } = 20f;
        public int LightMax { get; set; } = 50000;
        public int LightMin { get; set; } = 100;
        public int CO2Max { get; set; } = 1000;
        public int CO2Min { get; set; } = 400;
    }
}
