using Avalonia.Controls;
using SmartAgriculture.ViewModels;

namespace SmartAgriculture.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainWindowViewModel();
        }
    }
}
