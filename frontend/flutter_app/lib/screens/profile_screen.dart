import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Section
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Profile',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Manage your account',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            color: Colors.grey,
                          ),
                    ),
                  ],
                ),
              ),
              
              // Profile Info Section
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    const CircleAvatar(
                      radius: 50,
                      backgroundImage: AssetImage('assets/default_avatar.png'),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'John Doe',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'john.doe@example.com',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            color: Colors.grey,
                          ),
                    ),
                    const SizedBox(height: 24),
                    
                    // Profile Options
                    _buildProfileOption(
                      context: context,
                      icon: Icons.person,
                      color: Colors.blue,
                      title: 'Edit Profile',
                      subtitle: 'Update your personal information',
                      onTap: () {
                        // TODO: Implement edit profile
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildProfileOption(
                      context: context,
                      icon: Icons.notifications,
                      color: Colors.orange,
                      title: 'Notifications',
                      subtitle: 'Manage your notifications',
                      onTap: () {
                        // TODO: Implement notifications
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildProfileOption(
                      context: context,
                      icon: Icons.lock,
                      color: Colors.green,
                      title: 'Privacy & Security',
                      subtitle: 'Manage your account security',
                      onTap: () {
                        // TODO: Implement privacy settings
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildProfileOption(
                      context: context,
                      icon: Icons.settings,
                      color: Colors.purple,
                      title: 'Settings',
                      subtitle: 'App preferences and settings',
                      onTap: () {
                        // TODO: Implement settings
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildProfileOption(
                      context: context,
                      icon: Icons.help,
                      color: Colors.indigo,
                      title: 'Help & Support',
                      subtitle: 'Get help and contact support',
                      onTap: () {
                        // TODO: Navigate to support screen
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildProfileOption(
                      context: context,
                      icon: Icons.logout,
                      color: Colors.red,
                      title: 'Log Out',
                      subtitle: 'Sign out of your account',
                      onTap: () {
                        // TODO: Implement logout
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProfileOption({
    required BuildContext context,
    required IconData icon,
    required Color color,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: color.withOpacity(0.1),
                child: Icon(icon, color: color),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: Colors.grey,
                          ),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: Colors.grey),
            ],
          ),
        ),
      ),
    );
  }
}