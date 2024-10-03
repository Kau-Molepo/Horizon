import 'package:flutter/material.dart';
import 'application_screen.dart'; 
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
  // List of screens corresponding to the navigation items
  final List<Widget> _screens = const [
    AnalyticsScreen(key: ValueKey('AnalyticsScreen')),
    PayrollScreen(key: ValueKey('PayrollScreen')),
    HrScreen(key: ValueKey('HrScreen')),
    SupportScreen(key: ValueKey('SupportScreen')),
    DocumentUploadScreen(key: ValueKey('DocumentUploadScreen')),
  ];

  int _currentIndex = 0; // Track the current screen index
  bool _isDarkMode = false; // Track dark mode state

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: _isDarkMode ? ThemeData.dark() : ThemeData.light(),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Dashboard'),
          backgroundColor: _isDarkMode ? Colors.black : Colors.blueAccent,
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
            _buildDrawer(), // Build the navigation drawer (left side)
            Expanded(
              child: SafeArea(
                child: AnimatedSwitcher(
                  duration: const Duration(milliseconds: 300), // Smooth transition
                  child: _screens[_currentIndex], // Display the current screen
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
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.zero), // Remove rounding
        child: Column(
          children: [
            _buildDrawerHeader(), // Header of the drawer
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  _buildDrawerItem(Icons.trending_up, 'Analytics', 0),
                  _buildDrawerItem(Icons.attach_money, 'Payroll', 1),
                  _buildDrawerItem(Icons.people, 'HR', 2),
                  _buildDrawerItem(Icons.support, 'Support', 3),
                  _buildDrawerItem(Icons.upload_file, 'Documents', 4),
                  _buildDrawerItem(Icons.person, 'Profile', -1), // Profile under construction
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
        color: _isDarkMode ? Colors.black54 : Colors.blueAccent,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CircleAvatar(
            backgroundImage: const NetworkImage('https://via.placeholder.com/150'), // Placeholder image
            radius: 40,
          ),
          const SizedBox(height: 10),
          const Text('Welcome, John Doe', style: TextStyle(color: Colors.white, fontSize: 16)),
        ],
      ),
    );
  }

  Widget _buildDrawerItem(IconData icon, String label, int index) {
    final isActive = _currentIndex == index; // Check if the item is active
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

  Widget _buildUserProfile() {
    return Drawer(
      child: Container(
        width: 250, // Fixed width for the user profile section
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
                Navigator.pushNamed(context, '/editProfile'); // Navigate to edit profile screen
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blueAccent,
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              ),
              child: const Text('Edit Profile'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushReplacementNamed(context, '/login'); // Navigate to login screen
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.redAccent,
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              ),
              child: const Text('Log Out'),
            ),
          ],
        ),
      ),
    );
  }
}
