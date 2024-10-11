import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class PayrollScreen extends StatefulWidget {
  const PayrollScreen({Key? key}) : super(key: key);

  @override
  _PayrollScreenState createState() => _PayrollScreenState();
}

class _PayrollScreenState extends State<PayrollScreen> {
  final List<Employee> _employees = [];
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _hoursController = TextEditingController();
  final TextEditingController _rateController = TextEditingController();

  UserRole? _userRole;

  @override
  void initState() {
    super.initState();
    _getUserRole();
  }

  Future<void> _getUserRole() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      int? userId = prefs.getInt('user_id');

      if (userId != null) {
        final response = await http.get(
          Uri.parse('http://127.0.0.1:8000/users/user?user_id=$userId'),
          headers: {'Content-Type': 'application/json'},
        );

        if (response.statusCode == 200) {
          final userData = json.decode(response.body);
          setState(() {
            _userRole = _mapUserRole(userData['role']);
          });
        } else {
          throw Exception('Failed to load user data (status: ${response.statusCode})');
        }
      } else {
        throw Exception('User ID not found in SharedPreferences');
      }
    } catch (e) {
      print('Error getting user role: $e');
      setState(() => _userRole = null);
      _showErrorDialog('Error fetching user data. Please try again.');
    }
  }

  UserRole _mapUserRole(String role) {
    switch (role) {
      case 'admin':
        return UserRole.Admin;
      case 'manager':
        return UserRole.Manager;
      case 'employee':
        return UserRole.Employee;
      default:
        throw Exception('Unknown role: $role');
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Payroll Management'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: _userRole == null
            ? const Center(child: CircularProgressIndicator())
            : _buildRoleSpecificContent(),
      ),
    );
  }

  Widget _buildRoleSpecificContent() {
    switch (_userRole!) {
      case UserRole.Admin:
        return _buildAdminView();
      case UserRole.Manager:
        return _buildManagerView();
      case UserRole.Employee:
        return _buildEmployeeView();
      default:
        return const Text("Unknown role");
    }
  }

  Widget _buildAdminView() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Admin Overview',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        _buildEmployeeForm(),
        const SizedBox(height: 20),
        _buildEmployeeList(),
      ],
    );
  }

  Widget _buildManagerView() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Manager Overview',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        _buildEmployeeList(),
      ],
    );
  }

  Widget _buildEmployeeView() {
    final employee = Employee(name: 'John Doe', hoursWorked: 40, hourlyRate: 25);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Employee Payroll',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        ListTile(
          title: Text(employee.name),
          subtitle: Text('Hours Worked: ${employee.hoursWorked} | Hourly Rate: \$${employee.hourlyRate.toStringAsFixed(2)}'),
          trailing: Text(
            'Gross Salary: \$${employee.calculateGrossSalary().toStringAsFixed(2)}',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
      ],
    );
  }

  Widget _buildEmployeeForm() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Add Employee',
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        _buildTextField(_nameController, 'Employee Name'),
        const SizedBox(height: 10),
        _buildTextField(_hoursController, 'Hours Worked', isNumber: true),
        const SizedBox(height: 10),
        _buildTextField(_rateController, 'Hourly Rate', isNumber: true),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: _addEmployee,
          child: const Text('Add Employee'),
        ),
      ],
    );
  }

  Widget _buildTextField(TextEditingController controller, String labelText, {bool isNumber = false}) {
    return TextField(
      controller: controller,
      keyboardType: isNumber ? TextInputType.number : TextInputType.text,
      decoration: InputDecoration(
        border: const OutlineInputBorder(),
        labelText: labelText,
      ),
    );
  }

  Widget _buildEmployeeList() {
    if (_employees.isEmpty) {
      return const Center(child: Text('No employees added.'));
    }

    return Expanded(
      child: ListView.builder(
        itemCount: _employees.length,
        itemBuilder: (context, index) {
          final employee = _employees[index];
          return ListTile(
            title: Text(employee.name),
            subtitle: Text('Hours Worked: ${employee.hoursWorked} | Hourly Rate: \$${employee.hourlyRate.toStringAsFixed(2)}'),
            trailing: Text(
              'Gross Salary: \$${employee.calculateGrossSalary().toStringAsFixed(2)}',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          );
        },
      ),
    );
  }

  void _addEmployee() {
    final String name = _nameController.text;
    final double? hoursWorked = double.tryParse(_hoursController.text);
    final double? hourlyRate = double.tryParse(_rateController.text);

    if (name.isEmpty || hoursWorked == null || hourlyRate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter valid employee details.')),
      );
      return;
    }

    final newEmployee = Employee(name: name, hoursWorked: hoursWorked, hourlyRate: hourlyRate);
    setState(() {
      _employees.add(newEmployee);
      _nameController.clear();
      _hoursController.clear();
      _rateController.clear();
    });
  }
}

class Employee {
  final String name;
  final double hoursWorked;
  final double hourlyRate;

  Employee({
    required this.name,
    required this.hoursWorked,
    required this.hourlyRate,
  });

  double calculateGrossSalary() {
    return hoursWorked * hourlyRate;
  }
}

enum UserRole { Admin, Manager, Employee }

void main() {
  runApp(const MaterialApp(
    home: PayrollScreen(),
  ));
}
