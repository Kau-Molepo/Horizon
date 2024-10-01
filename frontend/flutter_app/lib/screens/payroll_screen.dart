import 'package:flutter/material.dart';

class PayrollScreen extends StatelessWidget {
  const PayrollScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Payroll')),
      body: Center(
        child: Text('Payroll information goes here'),
      ),
    );
  }
}
