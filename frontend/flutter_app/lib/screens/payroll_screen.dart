import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import 'dart:convert';
import 'dart:math';

class PayrollScreen extends StatefulWidget {
  const PayrollScreen({super.key});

  @override
  _PayrollScreenState createState() => _PayrollScreenState();
}

class _PayrollScreenState extends State<PayrollScreen> with SingleTickerProviderStateMixin {
  final List<Employee> _employees = [];
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _hoursController = TextEditingController();
  final TextEditingController _rateController = TextEditingController();
  final TextEditingController _overtimeController = TextEditingController();
  final TextEditingController _bonusController = TextEditingController();
  final TextEditingController _searchController = TextEditingController();
  
  late TabController _tabController;
  final _currencyFormatter = NumberFormat.currency(symbol: '\$');
  
  UserRole? _userRole;
  bool _isLoading = false;
  bool _isGridView = false;
  String _selectedPayPeriod = 'Weekly';
  String _selectedDepartment = 'Engineering';
  bool _includeOvertime = false;
  bool _includeBonus = false;
  DateTime _selectedDate = DateTime.now();
  
  final List<String> _payPeriods = ['Weekly', 'Bi-Weekly', 'Monthly'];
  final List<String> _departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'];
  final List<String> _exportOptions = ['PDF', 'CSV', 'Excel'];
  
  // Filter states
  Set<String> _selectedDepartmentFilters = {};
  RangeValues _salaryRange = const RangeValues(0, 100000);
  
  // Settings
  bool _enableNotifications = true;
  bool _enableAutoSave = true;
  bool _showTaxCalculations = false;

  final List<FlSpot> _payrollTrend = [
    const FlSpot(0, 45000),
    const FlSpot(1, 48000),
    const FlSpot(2, 47000),
    const FlSpot(3, 49000),
    const FlSpot(4, 52000),
    const FlSpot(5, 53000),
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _getUserRole();
    _loadSampleEmployees();
    _loadPreferences();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _nameController.dispose();
    _hoursController.dispose();
    _rateController.dispose();
    _overtimeController.dispose();
    _bonusController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _loadSampleEmployees() {
    _employees.addAll([
      Employee(
        name: 'John Doe',
        hoursWorked: 40,
        hourlyRate: 25,
        overtimeHours: 5,
        department: 'Engineering',
        bonus: 1000,
      ),
      Employee(
        name: 'Jane Smith',
        hoursWorked: 38,
        hourlyRate: 30,
        overtimeHours: 3,
        department: 'Marketing',
        bonus: 800,
      ),
    ]);
  }

  Future<void> _loadPreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      setState(() {
        _enableNotifications = prefs.getBool('enableNotifications') ?? true;
        _enableAutoSave = prefs.getBool('enableAutoSave') ?? true;
        _showTaxCalculations = prefs.getBool('showTaxCalculations') ?? false;
        _isGridView = prefs.getBool('isGridView') ?? false;
      });
    } catch (e) {
      _showErrorDialog('Error loading preferences');
    }
  }

  Future<void> _getUserRole() async {
    setState(() => _isLoading = true);
    try {
      final prefs = await SharedPreferences.getInstance();
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
      }
    } catch (e) {
      _showErrorDialog('Error fetching user data. Please try again.');
      setState(() => _userRole = null);
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
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

  UserRole _mapUserRole(String role) {
    switch (role.toLowerCase()) {
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

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Payroll Management'),
          bottom: TabBar(
            controller: _tabController,
            tabs: const [
              Tab(icon: Icon(Icons.dashboard), text: 'Overview'),
              Tab(icon: Icon(Icons.people), text: 'Employees'),
              Tab(icon: Icon(Icons.settings), text: 'Settings'),
            ],
          ),
          actions: _buildAppBarActions(),
        ),
        body: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : TabBarView(
                controller: _tabController,
                children: [
                  _buildOverviewTab(),
                  _buildEmployeesTab(),
                  _buildSettingsTab(),
                ],
              ),
        floatingActionButton: _buildFloatingActionButton(),
      ),
    );
  }

  List<Widget> _buildAppBarActions() {
    return [
      IconButton(
        icon: Icon(_isGridView ? Icons.list : Icons.grid_view),
        onPressed: () => setState(() => _isGridView = !_isGridView),
      ),
      PopupMenuButton<String>(
        icon: const Icon(Icons.file_download),
        onSelected: _handleExport,
        itemBuilder: (context) => _exportOptions
            .map((option) => PopupMenuItem(
                  value: option,
                  child: Text('Export as $option'),
                ))
            .toList(),
      ),
    ];
  }

  Widget _buildOverviewTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildQuickStats(),
          const SizedBox(height: 20),
          _buildPayrollTrendChart(),
          if (_showTaxCalculations) ...[
            const SizedBox(height: 20),
            _buildTaxSummary(),
          ],
        ],
      ),
    );
  }

  Widget _buildQuickStats() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Quick Stats - ${DateFormat('MMMM yyyy').format(_selectedDate)}',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildStatItem('Total Payroll', _calculateTotalPayroll()),
                _buildStatItem('Total Employees', _employees.length.toString()),
                _buildStatItem('Average Salary', _calculateAverageSalary()),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(String label, String value) {
    return Expanded(
      child: Column(
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.titleSmall,
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
          ),
        ],
      ),
    );
  }

  String _calculateTotalPayroll() {
    double total = _employees.fold(0, (sum, emp) {
      return sum + (emp.hourlyRate * emp.hoursWorked) +
          (emp.overtimeHours * emp.hourlyRate * 1.5) +
          emp.bonus;
    });
    return _currencyFormatter.format(total);
  }

  String _calculateAverageSalary() {
    if (_employees.isEmpty) return _currencyFormatter.format(0);
    double total = _employees.fold(0, (sum, emp) {
      return sum + (emp.hourlyRate * 2080); // 2080 = 40 hours * 52 weeks
    });
    double average = total / _employees.length;
    return _currencyFormatter.format(average);
  }

  Widget _buildPayrollTrendChart() {
    return LineChart(
      LineChartData(
        gridData: FlGridData(show: false),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          LineChartBarData(
            spots: _payrollTrend,
            isCurved: true,
            colors: [Colors.blue],
            belowBarData: BarAreaData(show: false),
          ),
        ],
      ),
    );
  }

  Widget _buildTaxSummary() {
    // Example Tax Summary widget
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: const [
            Text(
              'Tax Summary',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            Text('Estimated Taxes: \$5000'),
            Text('Tax Withheld: \$3000'),
          ],
        ),
      ),
    );
  }

  Widget _buildEmployeesTab() {
    return Column(
      children: [
        _buildEmployeeSearchBar(),
        Expanded(child: _isGridView ? _buildEmployeeGrid() : _buildEmployeeList()),
      ],
    );
  }

  Widget _buildEmployeeSearchBar() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: TextField(
        controller: _searchController,
        decoration: const InputDecoration(
          labelText: 'Search Employees',
          border: OutlineInputBorder(),
        ),
        onChanged: (query) {
          setState(() {});
        },
      ),
    );
  }

  Widget _buildEmployeeList() {
    var filteredEmployees = _employees
        .where((emp) => emp.name.toLowerCase().contains(_searchController.text.toLowerCase()))
        .toList();

    return ListView.builder(
      itemCount: filteredEmployees.length,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text(filteredEmployees[index].name),
          subtitle: Text('Department: ${filteredEmployees[index].department}'),
          onTap: () => _showEmployeeDetails(filteredEmployees[index]),
        );
      },
    );
  }

  Widget _buildEmployeeGrid() {
    var filteredEmployees = _employees
        .where((emp) => emp.name.toLowerCase().contains(_searchController.text.toLowerCase()))
        .toList();

    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
      ),
      itemCount: filteredEmployees.length,
      itemBuilder: (context, index) {
        return Card(
          child: InkWell(
            onTap: () => _showEmployeeDetails(filteredEmployees[index]),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(filteredEmployees[index].name),
                Text('Dept: ${filteredEmployees[index].department}'),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showEmployeeDetails(Employee employee) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(employee.name),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Department: ${employee.department}'),
            Text('Hours Worked: ${employee.hoursWorked}'),
            Text('Hourly Rate: \$_${employee.hourlyRate}'),
            Text('Overtime: ${employee.overtimeHours} hours'),
            Text('Bonus: \$_${employee.bonus}'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsTab() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SwitchListTile(
            title: const Text('Enable Notifications'),
            value: _enableNotifications,
            onChanged: (value) async {
              setState(() {
                _enableNotifications = value;
              });
              final prefs = await SharedPreferences.getInstance();
              prefs.setBool('enableNotifications', value);
            },
          ),
          SwitchListTile(
            title: const Text('Auto-Save Changes'),
            value: _enableAutoSave,
            onChanged: (value) async {
              setState(() {
                _enableAutoSave = value;
              });
              final prefs = await SharedPreferences.getInstance();
              prefs.setBool('enableAutoSave', value);
            },
          ),
          SwitchListTile(
            title: const Text('Show Tax Calculations'),
            value: _showTaxCalculations,
            onChanged: (value) async {
              setState(() {
                _showTaxCalculations = value;
              });
              final prefs = await SharedPreferences.getInstance();
              prefs.setBool('showTaxCalculations', value);
            },
          ),
        ],
      ),
    );
  }

  void _handleExport(String format) {
    // Logic to handle export, for now just print
    print('Exporting data as $format');
  }

  FloatingActionButton _buildFloatingActionButton() {
    return FloatingActionButton(
      onPressed: () => _showAddEmployeeForm(),
      child: const Icon(Icons.add),
    );
  }

  void _showAddEmployeeForm() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add Employee'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: _hoursController,
              decoration: const InputDecoration(labelText: 'Hours Worked'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _rateController,
              decoration: const InputDecoration(labelText: 'Hourly Rate'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _overtimeController,
              decoration: const InputDecoration(labelText: 'Overtime Hours'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _bonusController,
              decoration: const InputDecoration(labelText: 'Bonus'),
              keyboardType: TextInputType.number,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _addEmployee();
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _addEmployee() {
    // Add a new employee to the list
    Employee newEmployee = Employee(
      name: _nameController.text,
      hoursWorked: double.parse(_hoursController.text),
      hourlyRate: double.parse(_rateController.text),
      overtimeHours: double.parse(_overtimeController.text),
      bonus: double.parse(_bonusController.text),
    );

    setState(() {
      _employees.add(newEmployee);
    });

    _clearTextFields();
  }

  void _clearTextFields() {
    _nameController.clear();
    _hoursController.clear();
    _rateController.clear();
    _overtimeController.clear();
    _bonusController.clear();
  }
}

class Employee {
  String name;
  double hoursWorked;
  double hourlyRate;
  double overtimeHours;
  double bonus;
  String department;

  Employee({
    required this.name,
    required this.hoursWorked,
    required this.hourlyRate,
    required this.overtimeHours,
    required this.bonus,
    this.department = 'Engineering',
  });
}

enum UserRole {
  Admin,
  Manager,
  Employee,
}
