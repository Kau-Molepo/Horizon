import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class PayrollScreen extends StatefulWidget {
  const PayrollScreen({super.key});

  @override
  _PayrollScreenState createState() => _PayrollScreenState();
}

class _PayrollScreenState extends State<PayrollScreen> {
  final List<Employee> _employees = [];
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _hoursController = TextEditingController();
  final TextEditingController _rateController = TextEditingController();
  UserRole? _userRole;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _getUserRole();
  }

  Future<void> _getUserRole() async {
    setState(() => _isLoading = true);
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
          setState(() => _userRole = _mapUserRole(userData['role']));
        } else {
          throw Exception('Failed to load user data');
        }
      } else {
        throw Exception('User ID not found in SharedPreferences');
      }
    } catch (e) {
      print('Error getting user role: $e');
      setState(() => _userRole = null);
      _showErrorDialog('Error fetching user data. Please try again.');
    } finally {
      setState(() => _isLoading = false);
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
    return SafeArea(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : _userRole == null
                  ? const Center(child: Text('No user role found.'))
                  : Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildHeader(),
                        const SizedBox(height: 20),
                        _buildRoleSpecificContent(),
                      ],
                    ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Payroll Dashboard',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                fontWeight: FontWeight.bold,
              ),
        ),
        const SizedBox(height: 8),
        Text(
          'Role: ${_userRole.toString().split('.').last}',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                color: Colors.grey,
              ),
        ),
      ],
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
        _buildEmployeeForm(),
        const SizedBox(height: 20),
        _buildEmployeeList(),
      ],
    );
  }

  Widget _buildManagerView() {
    return _buildEmployeeList();
  }

  Widget _buildEmployeeView() {
    final employee = Employee(name: 'John Doe', hoursWorked: 40, hourlyRate: 25);
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Personal Payroll',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 20),
            _buildPayrollMetrics(employee),
            const SizedBox(height: 20),
            _buildPayrollDetails(employee),
          ],
        ),
      ),
    );
  }

  Widget _buildPayrollMetrics(Employee employee) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      crossAxisSpacing: 16.0,
      mainAxisSpacing: 16.0,
      children: [
        _buildMetricCard('Hours Worked', '${employee.hoursWorked}', Icons.access_time, Colors.blue),
        _buildMetricCard('Hourly Rate', '\$${employee.hourlyRate}', Icons.attach_money, Colors.green),
        _buildMetricCard('Gross Salary', '\$${employee.calculateGrossSalary()}', Icons.account_balance_wallet, Colors.purple),
        _buildMetricCard('Pay Period', 'Weekly', Icons.date_range, Colors.orange),
      ],
    );
  }

  Widget _buildMetricCard(String title, String value, IconData icon, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 32,
              color: color,
            ),
            const SizedBox(height: 8),
            Text(
              title,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              value,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPayrollDetails(Employee employee) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Payroll Details',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            _buildDetailItem('Regular Hours', '${employee.hoursWorked} hrs'),
            _buildDetailItem('Overtime Hours', '0 hrs'),
            _buildDetailItem('Regular Pay', '\$${employee.calculateGrossSalary()}'),
            _buildDetailItem('Overtime Pay', '\$0.00'),
            const Divider(height: 32),
            _buildDetailItem('Gross Pay', '\$${employee.calculateGrossSalary()}', isTotal: true),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailItem(String label, String value, {bool isTotal = false}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: isTotal
                ? const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)
                : const TextStyle(fontSize: 16),
          ),
          Text(
            value,
            style: isTotal
                ? const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)
                : const TextStyle(fontSize: 16),
          ),
        ],
      ),
    );
  }

  Widget _buildEmployeeForm() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Add Employee',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            _buildTextField(_nameController, 'Employee Name', Icons.person),
            const SizedBox(height: 12),
            _buildTextField(_hoursController, 'Hours Worked', Icons.timer, isNumber: true),
            const SizedBox(height: 12),
            _buildTextField(_rateController, 'Hourly Rate', Icons.attach_money, isNumber: true),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _addEmployee,
                icon: const Icon(Icons.add),
                label: const Text('Add Employee'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String labelText, IconData icon, {bool isNumber = false}) {
    return TextField(
      controller: controller,
      keyboardType: isNumber ? TextInputType.number : TextInputType.text,
      decoration: InputDecoration(
        prefixIcon: Icon(icon),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
        labelText: labelText,
        filled: true,
        fillColor: Colors.grey[50],
      ),
    );
  }

  Widget _buildEmployeeList() {
    if (_employees.isEmpty) {
      return Card(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const [
              Icon(Icons.people_outline, size: 48, color: Colors.grey),
              SizedBox(height: 16),
              Text(
                'No employees added yet',
                style: TextStyle(fontSize: 18, color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Employee List',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _employees.length,
              itemBuilder: (context, index) {
                final employee = _employees[index];
                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: Colors.blue.withOpacity(0.1),
                      child: const Icon(Icons.person, color: Colors.blue),
                    ),
                    title: Text(
                      employee.name,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      'Hours: ${employee.hoursWorked} | Rate: \$${employee.hourlyRate.toStringAsFixed(2)}',
                    ),
                    trailing: Text(
                      '\$${employee.calculateGrossSalary().toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.green,
                      ),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  void _addEmployee() {
    // Add Employee functionality
  }
}

class Employee {
  final String name;
  final double hoursWorked;
  final double hourlyRate;

  Employee({required this.name, required this.hoursWorked, required this.hourlyRate});

  double calculateGrossSalary() {
    return hoursWorked * hourlyRate;
  }
}

enum UserRole { Admin, Manager, Employee }