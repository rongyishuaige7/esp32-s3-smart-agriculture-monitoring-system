using System;
using System.Globalization;
using Avalonia.Data.Converters;

namespace SmartAgriculture.Converters
{
    /// <summary>
    /// 将 bool 转为中文「开」「关」，用于设备状态显示。
    /// </summary>
    public class BoolToOnOffConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is bool b) return b ? "开" : "关";
            return "关";
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
