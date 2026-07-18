using System;
using SmartAgriculture.Models;

namespace SmartAgriculture.Services
{
    /// <summary>
    /// Deterministic, explicitly marked demonstration values for the desktop
    /// UI. It is not sensor input and cannot be used for environment decisions.
    /// </summary>
    public static class DemoEnvironmentDataSource
    {
        public static SensorData CreateSample()
        {
            var phase = DateTime.UtcNow.Second / 60.0 * Math.PI * 2;
            return new SensorData
            {
                Temperature = (float)(24.5 + Math.Sin(phase) * 0.8),
                Humidity = (float)(58.0 + Math.Cos(phase) * 3.0),
                Light = 800,
                CO2 = 700,
                Pressure = 1012.4f,
                Timestamp = DateTime.Now,
                FanOn = false,
                LightOn = false,
            };
        }
    }
}
