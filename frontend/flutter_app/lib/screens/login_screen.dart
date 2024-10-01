import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isLoading = false; // To show a loading indicator while waiting for a response

  // FastAPI Login Function
  Future<void> _login() async {
    setState(() {
      _isLoading = true; // Start loading
    });

    // Define the API endpoint
    const String apiUrl = "http://127.0.0.1:8000/users/login"; // Replace with your FastAPI URL

    // Prepare the request body
    Map<String, dynamic> body = {
      'email': _emailController.text,
      'password': _passwordController.text,
    };

    try {
      // Send a POST request to the login endpoint
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(body),
      );

      // Check if the response is successful
      if (response.statusCode == 200) {
        // Parse the response body
        var jsonResponse = jsonDecode(response.body);

        // If login is successful, navigate to the Dashboard
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const DashboardScreen()),
        );
      } else {
        // If the login fails, show an error message
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Invalid email or password')),
        );
      }
    } catch (error) {
      // Handle network or other errors
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $error')),
      );
    } finally {
      setState(() {
        _isLoading = false; // Stop loading
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black87, // Matching theme with splash screen
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 50),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Login",
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            const SizedBox(height: 40),

            // Email Input Field
            TextField(
              controller: _emailController,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.email, color: Colors.white),
                labelText: 'Email',
                labelStyle: const TextStyle(color: Colors.white70),
                filled: true,
                fillColor: Colors.grey[800],
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.white30),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.white),
                ),
              ),
              style: const TextStyle(color: Colors.white),
            ),
            const SizedBox(height: 20),

            // Password Input Field
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.lock, color: Colors.white),
                labelText: 'Password',
                labelStyle: const TextStyle(color: Colors.white70),
                filled: true,
                fillColor: Colors.grey[800],
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.white30),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Colors.white),
                ),
              ),
              style: const TextStyle(color: Colors.white),
            ),
            const SizedBox(height: 40),

            // Login Button with Loading Indicator
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _login, // Call the login function
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blueAccent,
                      padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 15),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text(
                      'Login',
                      style: TextStyle(color: Colors.white, fontSize: 18),
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}
