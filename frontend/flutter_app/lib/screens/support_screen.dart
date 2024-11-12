import 'package:flutter/material.dart';

class SupportScreen extends StatelessWidget {
  const SupportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Support',
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'How can we help you?',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            color: Colors.grey,
                          ),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    _buildSupportOption(
                      context: context,
                      icon: Icons.chat,
                      color: Colors.blue,
                      title: 'Live Chat',
                      subtitle: 'Chat with our support team',
                      onTap: () {
                        // TODO: Implement live chat
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildSupportOption(
                      context: context,
                      icon: Icons.email,
                      color: Colors.green,
                      title: 'Email Support',
                      subtitle: 'Send us an email',
                      onTap: () {
                        // TODO: Implement email support
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildSupportOption(
                      context: context,
                      icon: Icons.phone,
                      color: Colors.orange,
                      title: 'Call Support',
                      subtitle: 'Call our support line',
                      onTap: () {
                        // TODO: Implement call support
                      },
                    ),
                    const SizedBox(height: 16),
                    _buildSupportOption(
                      context: context,
                      icon: Icons.help,
                      color: Colors.purple,
                      title: 'FAQs',
                      subtitle: 'Browse frequently asked questions',
                      onTap: () {
                        // TODO: Implement FAQs
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

  Widget _buildSupportOption({
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