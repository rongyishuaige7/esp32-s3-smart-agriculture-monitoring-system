using System;
using System.Globalization;
using Avalonia.Data.Converters;

namespace SmartAgriculture.Converters
{
    /// <summary>
    /// Converts DateTime to DateTimeOffset? for Avalonia DatePicker binding.
    /// </summary>
    public class DateTimeToOffsetConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is DateTime dt)
                return new DateTimeOffset(dt);
            return null;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is DateTimeOffset dto)
                return dto.DateTime;
            if (value == null)
                return default(DateTime);
            return default(DateTime);
        }
    }
}
