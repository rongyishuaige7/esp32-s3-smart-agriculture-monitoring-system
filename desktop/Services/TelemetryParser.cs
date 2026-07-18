using System;
using System.Text.Json;
using SmartAgriculture.Models;

namespace SmartAgriculture.Services
{
    /// <summary>
    /// Parser for a line-oriented, unauthenticated teaching-prototype telemetry
    /// format. Network listening and device commands are intentionally absent
    /// from the public desktop application.
    /// </summary>
    public static class TelemetryParser
    {
        public static bool TryParseSensorJson(string json, out SensorData data)
        {
            data = null;
            if (string.IsNullOrWhiteSpace(json) || json.Length > 4096)
                return false;

            try
            {
                using var document = JsonDocument.Parse(json);
                var root = document.RootElement;
                if (root.ValueKind != JsonValueKind.Object)
                    return false;

                data = new SensorData
                {
                    UserId = 0,
                    Temperature = ReadFloat(root, "temperature"),
                    Humidity = ReadFloat(root, "humidity"),
                    Light = ReadInt(root, "light"),
                    CO2 = ReadInt(root, "co2"),
                    Pressure = ReadFloat(root, "pressure"),
                    FanOn = false,
                    LightOn = false,
                    Timestamp = DateTime.Now,
                };
                return true;
            }
            catch (JsonException)
            {
                return false;
            }
        }

        private static float ReadFloat(JsonElement root, string name)
        {
            return root.TryGetProperty(name, out var value) && value.TryGetSingle(out var number)
                ? number : 0;
        }

        private static int ReadInt(JsonElement root, string name)
        {
            return root.TryGetProperty(name, out var value) && value.TryGetInt32(out var number)
                ? number : 0;
        }
    }
}
