import 'package:flutter/material.dart';

class DocumentUploadScreen extends StatelessWidget {
  const DocumentUploadScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Document Upload')),
      body: Center(
        child: Text('Upload and view documents here'),
      ),
    );
  }
}
