import 'package:flutter/material.dart';

class HrScreen extends StatelessWidget {
  const HrScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('HR Services')),
      body: Center(
        child: Text('HR-related services go here'),
      ),
    );
  }
}
