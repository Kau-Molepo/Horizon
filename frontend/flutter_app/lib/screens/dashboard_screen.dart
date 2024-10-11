import 'package:flutter/material.dart';
import 'package:flutter_app/screens/login_screen.dart';
import 'application_screen.dart';
import 'profile_screen.dart';
import 'payroll_screen.dart';
import 'hr_screen.dart';
import 'support_screen.dart';
import 'document_upload_screen.dart';
import 'analytics_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final List<Widget> _screens = const [
    AnalyticsScreen(key: ValueKey('AnalyticsScreen')),
    PayrollScreen(key: ValueKey('PayrollScreen')),
    HrScreen(key: ValueKey('HrScreen')),
    SupportScreen(key: ValueKey('SupportScreen')),
    DocumentUploadScreen(key: ValueKey('DocumentUploadScreen')),
    ProfileScreen(key: ValueKey('ProfileScreen')),
  ];

  int _currentIndex = 0; // Track the current screen index
  bool _isDarkMode = false; // Track dark mode state

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: _isDarkMode ? ThemeData.dark() : ThemeData.light(),
      home: Scaffold(
        appBar: AppBar(
          backgroundColor: _isDarkMode ? Colors.black : Colors.blueAccent,
          title: Container(
            width: double.infinity,
            alignment: Alignment.center,
            child: const Text(
              'Horizon',
              style: TextStyle(
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          actions: [
            IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Settings not implemented yet")),
                );
              },
            ),
          ],
        ),
        body: Row(
          children: [
            _buildDrawer(),
            Expanded(
              child: SafeArea(
                child: AnimatedSwitcher(
                  duration: const Duration(milliseconds: 300),
                  child: _screens[_currentIndex],
                ),
              ),
            ),
            _buildSettingsDrawer(), // Add the settings drawer here
          ],
        ),
        endDrawer: _buildSettingsDrawer(), // Use the settings drawer here
        drawerScrimColor: Colors.transparent,
      ),
    );
  }

  Widget _buildDrawer() {
    return Container(
      width: 250,
      color: _isDarkMode ? Colors.grey[850] : Colors.blueGrey[800],
      child: Drawer(
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 16.0),
              child: _buildDrawerHeader('Dashboard'),
            ),
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  _buildDrawerItem(Icons.trending_up, 'Analytics', 0),
                  _buildDrawerItem(Icons.attach_money, 'Payroll', 1),
                  _buildDrawerItem(Icons.people, 'HR', 2),
                  _buildDrawerItem(Icons.support, 'Support', 3),
                  _buildDrawerItem(Icons.upload_file, 'Documents', 4),
                  _buildDrawerItem(Icons.person, 'Profile', 5),
                ],
              ),
            ),
            _buildThemeToggle(),
          ],
        ),
      ),
    );
  }

  Widget _buildDrawerHeader(String title) {
    return DrawerHeader(
      decoration: BoxDecoration(
        color: _isDarkMode ? Colors.black54 : Colors.blueAccent,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          CircleAvatar(
            backgroundImage: const NetworkImage('https://via.placeholder.com/150'),
            radius: 40,
          ),
        ],
      ),
    );
  }

  Widget _buildDrawerItem(IconData icon, String label, int index) {
    final isActive = _currentIndex == index;
    return Tooltip(
      message: label,
      child: ListTile(
        leading: Icon(icon, color: isActive ? Colors.blueAccent : (_isDarkMode ? Colors.white : Colors.grey[850])),
        title: Text(
          label,
          style: TextStyle(
            color: isActive ? Colors.blueAccent : (_isDarkMode ? Colors.white : Colors.grey[850]),
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
          ),
        ),
        tileColor: isActive ? (_isDarkMode ? Colors.blueGrey[900] : Colors.blue[50]) : Colors.transparent,
        onTap: () {
          if (index >= 0) {
            setState(() {
              _currentIndex = index; // Update current index
            });
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text("Profile screen is under construction")),
            );
          }
        },
      ),
    );
  }

  Widget _buildThemeToggle() {
    return SwitchListTile(
      title: const Text('Dark Mode'),
      value: _isDarkMode,
      onChanged: (bool value) {
        setState(() {
          _isDarkMode = value; // Toggle dark mode
        });
      },
      secondary: Icon(Icons.brightness_6, color: _isDarkMode ? Colors.white : Colors.grey[850]),
    );
  }

  Widget _buildSettingsDrawer() {
    return Container(
      width: 250,
      color: _isDarkMode ? Colors.grey[850] : Colors.blueGrey[800],
      child: Drawer(
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero),
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 16.0),
              child: _buildDrawerHeader('Settings'), // Header for settings drawer
            ),
            const SizedBox(height: 16),
            _buildSettingsDrawerItem(Icons.notifications, 'Notifications', () {
              // Handle notification preferences tap
            }),
            _buildSettingsDrawerItem(Icons.language, 'App Language', () {
              // Handle app language settings tap
            }),
            _buildSettingsDrawerItem(Icons.privacy_tip, 'Privacy Policy', () {
              // Handle privacy policy tap
            }),
            _buildSettingsDrawerItem(Icons.info, 'About Us', () {
              // Handle about us tap
            }),
            const Spacer(),
            const SizedBox(height: 16), // Spacing before log out button
            Padding(
              padding: const EdgeInsets.only(bottom: 16.0), // Added padding to the bottom
              child: ElevatedButton(
                onPressed: () {
                  // Navigate to Dashboard after login
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const LoginScreen()));
                  // Handle logout
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Logged out")),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.redAccent,
                  padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                ),
                child: const Text('Log Out'),
              ),
            ),
          ],
        ),
      ),
    );
  }


  Widget _buildSettingsDrawerItem(IconData icon, String label, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: _isDarkMode ? Colors.white : Colors.grey[850]),
      title: Text(label, style: const TextStyle(fontSize: 16)),
      onTap: onTap,
    );
  }
}
