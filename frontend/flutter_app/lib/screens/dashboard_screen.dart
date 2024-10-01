import 'package:flutter/material.dart';
import 'application_screen.dart'; // Define the respective screens for each module
import 'payroll_screen.dart';
import 'hr_screen.dart';
import 'support_screen.dart';
import 'document_upload_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Use MediaQuery to get screen dimensions
    final size = MediaQuery.of(context).size;

    // Adjust the number of columns based on screen width
    int crossAxisCount = size.width > 600 ? 3 : 2; // 3 columns for wide screens, 2 for narrow screens
    double aspectRatio = size.width > 600 ? 1.2 : 1.0; // Adjust the aspect ratio to ensure it looks good

    return Scaffold(
      appBar: AppBar(
        title: const Text('Employee Dashboard'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.count(
          crossAxisCount: crossAxisCount,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: aspectRatio,
          children: [
            _buildDashboardItem(
              context,
              icon: Icons.apps,
              label: "Applications",
              onTap: () => Navigator.push(
                context, MaterialPageRoute(builder: (context) => const ApplicationScreen())
              ),
            ),
            _buildDashboardItem(
              context,
              icon: Icons.attach_money,
              label: "Payroll",
              onTap: () => Navigator.push(
                context, MaterialPageRoute(builder: (context) => const PayrollScreen())
              ),
            ),
            _buildDashboardItem(
              context,
              icon: Icons.people,
              label: "HR",
              onTap: () => Navigator.push(
                context, MaterialPageRoute(builder: (context) => const HrScreen())
              ),
            ),
            _buildDashboardItem(
              context,
              icon: Icons.support,
              label: "Support",
              onTap: () => Navigator.push(
                context, MaterialPageRoute(builder: (context) => const SupportScreen())
              ),
            ),
            _buildDashboardItem(
              context,
              icon: Icons.upload_file,
              label: "Documents",
              onTap: () => Navigator.push(
                context, MaterialPageRoute(builder: (context) => const DocumentUploadScreen())
              ),
            ),
            _buildDashboardItem(
              context,
              icon: Icons.person,
              label: "Profile",
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Profile screen is under construction"))
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  // Helper method to create a dashboard item
  Widget _buildDashboardItem(BuildContext context, {required IconData icon, required String label, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        color: Colors.blueGrey[50], // Keep consistent theme color
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 50, color: Colors.blueAccent),
              const SizedBox(height: 10),
              Text(label, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
            ],
          ),
        ),
      ),
    );
  }
}
