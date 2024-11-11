import 'package:flutter/material.dart';

class ApplicationScreen extends StatelessWidget {
  const ApplicationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Applications')),
      body: const Center(
        child: Text('Application access details go here'),
      ),
    );
  }
}
