import 'package:flutter/material.dart';

class HrScreen extends StatelessWidget {
  const HrScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'HR Services',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 24),
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                mainAxisSpacing: 16,
                crossAxisSpacing: 16,
                children: [
                  _buildServiceCard(
                    'Employee Directory',
                    Icons.people,
                    Colors.blue,
                    () {},
                  ),
                  _buildServiceCard(
                    'Leave Management',
                    Icons.calendar_today,
                    Colors.green,
                    () {},
                  ),
                  _buildServiceCard(
                    'Benefits',
                    Icons.health_and_safety,
                    Colors.orange,
                    () {},
                  ),
                  _buildServiceCard(
                    'Training',
                    Icons.school,
                    Colors.purple,
                    () {},
                  ),
                  _buildServiceCard(
                    'Performance',
                    Icons.trending_up,
                    Colors.red,
                    () {},
                  ),
                  _buildServiceCard(
                    'Recruitment',
                    Icons.person_add,
                    Colors.teal,
                    () {},
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildServiceCard(String title, IconData icon, Color color, VoidCallback onTap) {
    return Card(
      elevation: 4,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                icon,
                size: 48,
                color: color,
              ),
              const SizedBox(height: 8),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
