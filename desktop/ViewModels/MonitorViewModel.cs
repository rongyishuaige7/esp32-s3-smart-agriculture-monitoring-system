using System;
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using SmartAgriculture.Models;
using SmartAgriculture.Services;

namespace SmartAgriculture.ViewModels
{
    /// <summary>
    /// Public desktop teaching display. It holds in-memory demo data only: no
    /// account, database, TCP listener, device command or actuator control.
    /// </summary>
    public partial class MonitorViewModel : ObservableObject
    {
        private readonly Threshold _threshold = new Threshold();

        [ObservableProperty] private float _temperature;
        [ObservableProperty] private float _humidity;
        [ObservableProperty] private int _light;
        [ObservableProperty] private int _co2;
        [ObservableProperty] private float _pressure;
        [ObservableProperty] private string _lastUpdateTime = "尚未加载示例数据";
        [ObservableProperty] private bool _alertTemperature;
        [ObservableProperty] private bool _alertHumidity;
        [ObservableProperty] private bool _alertLight;
        [ObservableProperty] private bool _alertCo2;
        [ObservableProperty] private string _dataSourceStatus = "示例数据（非真机）；网络接收与设备控制公开默认关闭";

        public ObservableCollection<string> LogLines { get; } = new ObservableCollection<string>();

        public MonitorViewModel() => LoadDemoData();

        [RelayCommand]
        private void LoadDemoData()
        {
            Apply(DemoEnvironmentDataSource.CreateSample(), "已加载示例数据（非真机）。");
        }

        /// <summary>Code-level only parser for tests/teaching; it never opens a socket.</summary>
        public bool TryImportTeachingJson(string json)
        {
            if (!TelemetryParser.TryParseSensorJson(json, out var data))
            {
                AddLog("本地 JSON 解析失败：不代表设备或网络状态。");
                return false;
            }
            Apply(data, "已解析本地教学 JSON；不代表设备身份、实时性或真机数据。");
            return true;
        }

        private void Apply(SensorData data, string log)
        {
            Temperature = data.Temperature;
            Humidity = data.Humidity;
            Light = data.Light;
            Co2 = data.CO2;
            Pressure = data.Pressure;
            LastUpdateTime = DateTime.Now.ToString("HH:mm:ss");
            AlertTemperature = Temperature > _threshold.TempMax || Temperature < _threshold.TempMin;
            AlertHumidity = Humidity > _threshold.HumidityMax || Humidity < _threshold.HumidityMin;
            AlertLight = Light > _threshold.LightMax || Light < _threshold.LightMin;
            AlertCo2 = Co2 > _threshold.CO2Max || Co2 < _threshold.CO2Min;
            AddLog(log);
        }

        private void AddLog(string line)
        {
            LogLines.Insert(0, $"[{DateTime.Now:HH:mm:ss}] {line}");
            while (LogLines.Count > 100) LogLines.RemoveAt(LogLines.Count - 1);
        }
    }
}
