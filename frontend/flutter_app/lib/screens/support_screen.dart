import 'package:flutter/material.dart';

class SupportScreen extends StatelessWidget {
  const SupportScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Support'),
        backgroundColor: Theme.of(context).colorScheme.primary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'How can we help you?',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),
            ListTile(
              leading: const Icon(Icons.chat, color: Colors.blue),
              title: const Text('Live Chat'),
              subtitle: const Text('Chat with our support team'),
              onTap: () {
                // TODO: Implement live chat
              },
            ),
            ListTile(
              leading: const Icon(Icons.email, color: Colors.green),
              title: const Text('Email Support'),
              subtitle: const Text('Send us an email'),
              onTap: () {
                // TODO: Implement email support
              },
            ),
            ListTile(
              leading: const Icon(Icons.phone, color: Colors.orange),
              title: const Text('Call Support'),
              subtitle: const Text('Call our support line'),
              onTap: () {
                // TODO: Implement call support
              },
            ),
            ListTile(
              leading: const Icon(Icons.help, color: Colors.purple),
              title: const Text('FAQs'),
              subtitle: const Text('Browse frequently asked questions'),
              onTap: () {
                // TODO: Implement FAQs
              },
            ),
          ],
        ),
      ),
    );
  }
}
