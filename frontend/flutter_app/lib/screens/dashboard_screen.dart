import 'package:flutter/material.dart';
import 'application_screen.dart'; // Ensure these imports are correct
import 'payroll_screen.dart';
import 'hr_screen.dart';
import 'support_screen.dart';
import 'document_upload_screen.dart';
import 'analytics_screen.dart'; // Ensure all screen imports are valid

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  // List of screens corresponding to the navigation items
  final List<Widget> _screens = [
    const AnalyticsScreen(key: ValueKey('AnalyticsScreen')),
    const PayrollScreen(key: ValueKey('PayrollScreen')),
    const HrScreen(key: ValueKey('HrScreen')),
    const SupportScreen(key: ValueKey('SupportScreen')),
    const DocumentUploadScreen(key: ValueKey('DocumentUploadScreen')),
  ];

  int _currentIndex = 0; // Track the current screen index
  bool _isDarkMode = false; // Track dark mode state

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: _isDarkMode ? ThemeData.dark() : ThemeData.light(),
      home: Scaffold(
        body: Row(
          children: [
            _buildDrawer(), // Build the navigation drawer (left side)
            Expanded(
              child: SafeArea(
                child: Row(
                  children: [
                    Expanded(
                      child: AnimatedSwitcher(
                        duration: const Duration(milliseconds: 300), // Smooth transition
                        child: _screens[_currentIndex], // Display the current screen
                      ),
                    ),
                  ],
                ),
              ),
            ),
            _buildUserProfile(), // User profile on the right side
          ],
        ),
        drawer: _buildDrawer(), // Main navigation drawer on the left
        endDrawer: _buildUserProfile(), // User profile drawer on the right
        drawerScrimColor: Colors.transparent, // Ensures both drawers are visible simultaneously
      ),
    );
  }

  Widget _buildDrawer() {
    return Container(
      width: 250, // Fixed width for the drawer
      color: _isDarkMode ? Colors.grey[850] : Colors.blueGrey[800], // Darker background for the drawer
      child: Drawer(
        child: Column(
          children: [
            //_buildDrawerHeader(), // Header of the drawer
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  _buildDrawerItem(Icons.trending_up, 'Analytics', 0),
                  _buildDrawerItem(Icons.attach_money, 'Payroll', 1),
                  _buildDrawerItem(Icons.people, 'HR', 2),
                  _buildDrawerItem(Icons.support, 'Support', 3),
                  _buildDrawerItem(Icons.upload_file, 'Documents', 4),
                  _buildDrawerItem(Icons.person, 'Profile', -1), // -1 indicates under construction
                ],
              ),
            ),
            _buildThemeToggle(), // Theme toggle switch
          ],
        ),
      ),
    );
  }

  Widget _buildDrawerHeader() {
    return DrawerHeader(
      decoration: BoxDecoration(
        color: Colors.blueAccent,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            backgroundImage: NetworkImage('https://via.placeholder.com/150'), // Placeholder image
            radius: 40,
          ),
        ],
      ),
    );
  }

  Widget _buildDrawerItem(IconData icon, String label, int index) {
    final isActive = _currentIndex == index; // Check if the item is active
    return Tooltip(
      message: label,
      child: ListTile(
        leading: Icon(icon, color: _isDarkMode ? Colors.white : Colors.grey[850]),
        title: Text(
          label,
          style: TextStyle(
            color: _isDarkMode ? Colors.white : Colors.grey[850],
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
          ),
        ),
        tileColor: isActive ? Colors.blueAccent : Colors.transparent,
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
      secondary: const Icon(Icons.brightness_6),
    );
  }

  Widget _buildUserProfile() {
    return Drawer(
      child: Container(
        width: 300, // Fixed width for the user profile section
        padding: const EdgeInsets.all(16),
        color: _isDarkMode ? Colors.grey[850] : Colors.white,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildDrawerHeader(),
            const SizedBox(height: 16),
            const Text('Name: John Doe', style: TextStyle(fontSize: 16)),
            const Text('Role: Employee', style: TextStyle(fontSize: 16)),
            const Text('Email: john.doe@example.com', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Edit profile functionality goes here
                Navigator.pushNamed(context, '/editProfile'); // Replace with your actual edit profile route
              },
              child: const Text('Edit Profile'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Logout functionality goes here
                Navigator.pushReplacementNamed(context, '/login'); // Replace with your actual login route
              },
              child: const Text('Log Out'),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            ),
          ],
        ),
      ),
    );
  }
}