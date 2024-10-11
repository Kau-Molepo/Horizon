import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({Key? key}) : super(key: key);

  @override
  _AnalyticsScreenState createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  List<bool> _isSelected = [true, false];
  String _selectedFilter = 'Last 7 Days';
  UserRole? _userRole;

  @override
  void initState() {
    super.initState();
    _getUserRole();
  }

  Future<void> _getUserRole() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    int? userId = prefs.getInt('user_id');
    if (userId != null) {
      try {
        final response = await http.get(
          Uri.parse('http://127.0.0.1:8000/users/user?user_id=$userId'),
          headers: {'Content-Type': 'application/json'},
        );

        if (response.statusCode == 200) {
          final userData = json.decode(response.body);
          setState(() {
            _userRole = _getUserRoleFromResponse(userData);
          });
        } else {
          throw Exception('Failed to load user data: ${response.statusCode}');
        }
      } catch (e) {
        print('Error getting user role: $e');
        setState(() {
          _userRole = null;
        });
      }
    } else {
      print('User ID not found in SharedPreferences');
      setState(() {
        _userRole = null;
      });
    }
  }

  UserRole _getUserRoleFromResponse(Map<String, dynamic> userData) {
    switch (userData['role']) {
      case 'admin':
        return UserRole.Admin;
      case 'manager':
        return UserRole.Manager;
      case 'employee':
        return UserRole.Employee;
      default:
        throw Exception('Unknown role: ${userData['role']}');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_userRole == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Analytics Overview'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Analytics Overview',
                style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              const Text(
                'Here you can view your analytics data',
                style: TextStyle(fontSize: 18),
              ),
              const SizedBox(height: 20),
              _buildKPISection(),
              const SizedBox(height: 20),
              _buildDateFilters(),
              const SizedBox(height: 20),
              _buildMetricToggle(),
              const SizedBox(height: 20),
              // Role-Specific Graphs Section
              _buildRoleSpecificGraphs(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildKPISection() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildKPI('Total Sales', '\$5,000'),
        _buildKPI('Active Users', '1,230'),
        _buildKPI('Monthly Growth', '+15%'),
      ],
    );
  }

  Widget _buildKPI(String title, String value) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 4),
        Text(title, style: const TextStyle(fontSize: 16)),
      ],
    );
  }

  Widget _buildDateFilters() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        _buildFilterButton('Last 7 Days'),
        _buildFilterButton('Last Month'),
        _buildFilterButton('Year to Date'),
      ],
    );
  }

  Widget _buildFilterButton(String label) {
    return OutlinedButton(
      onPressed: () {
        setState(() {
          _selectedFilter = label;
        });
      },
      child: Text(
        label,
        style: TextStyle(
          color: _selectedFilter == label ? Colors.blue : Colors.black,
        ),
      ),
    );
  }

  Widget _buildMetricToggle() {
    return ToggleButtons(
      isSelected: _isSelected,
      children: const [
        Padding(padding: EdgeInsets.all(8.0), child: Text('User Activity')),
        Padding(padding: EdgeInsets.all(8.0), child: Text('Sales Data')),
      ],
      onPressed: (int index) {
        setState(() {
          for (int i = 0; i < _isSelected.length; i++) {
            _isSelected[i] = i == index;
          }
        });
      },
    );
  }

  Widget _buildRoleSpecificGraphs() {
    switch (_userRole!) {
      case UserRole.Admin:
        return _buildAdminGraphs();
      case UserRole.Manager:
        return _buildManagerGraphs();
      case UserRole.Employee:
        return _buildEmployeeGraphs();
      default:
        return const SizedBox.shrink();
    }
  }

  // Admin-Specific Graphs (Organization-wide, high-level KPIs)
  Widget _buildAdminGraphs() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 20),
        const Text(
          'Organization-Wide Performance',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        _buildPieChart(), // Example organization-wide distribution (e.g., revenue by region)
        const SizedBox(height: 20),
        _buildBarChart(), // Example high-level bar chart (e.g., department sales comparison)
      ],
    );
  }

  // Manager-Specific Graphs (Team or Department-specific metrics)
  Widget _buildManagerGraphs() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 20),
        const Text(
          'Team Performance Overview',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        _buildBarChart(), // Example bar chart (e.g., team performance comparison)
        const SizedBox(height: 20),
        _buildLineChart(), // Example line chart (e.g., team activity trends)
      ],
    );
  }

  // Employee-Specific Graphs (Individual performance metrics)
  Widget _buildEmployeeGraphs() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 20),
        const Text(
          'Your Performance Metrics',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        _buildLineChart(), // Example line chart (e.g., personal activity trends)
        const SizedBox(height: 20),
        _buildPieChart(), // Example pie chart (e.g., personal task distribution)
      ],
    );
  }

  // Charts (Reused Across Roles)
  Widget _buildPieChart() {
    return SizedBox(
      height: 250, // Fix the height
      child: PieChart(
        PieChartData(
          sections: [
            PieChartSectionData(
              value: 30,
              color: Colors.blue,
              title: 'Category A',
              radius: 50,
              titleStyle: const TextStyle(color: Colors.white, fontSize: 16),
            ),
            PieChartSectionData(
              value: 40,
              color: Colors.green,
              title: 'Category B',
              radius: 50,
              titleStyle: const TextStyle(color: Colors.white, fontSize: 16),
            ),
            PieChartSectionData(
              value: 30,
              color: Colors.red,
              title: 'Category C',
              radius: 50,
              titleStyle: const TextStyle(color: Colors.white, fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBarChart() {
    return SizedBox(
      height: 250, // Fix the height
      child: BarChart(
        BarChartData(
          titlesData: FlTitlesData(
            leftTitles: SideTitles(showTitles: true),
            bottomTitles: SideTitles(showTitles: true),
          ),
          borderData: FlBorderData(show: false),
          barGroups: [
            BarChartGroupData(x: 0, barRods: [BarChartRodData(y: 10, colors: [Colors.blue])]),
            BarChartGroupData(x: 1, barRods: [BarChartRodData(y: 15, colors: [Colors.green])]),
            BarChartGroupData(x: 2, barRods: [BarChartRodData(y: 20, colors: [Colors.red])]),
          ],
        ),
      ),
    );
  }

  Widget _buildLineChart() {
    return SizedBox(
      height: 250, // Fix the height
      child: LineChart(
        LineChartData(
          titlesData: FlTitlesData(
            leftTitles: SideTitles(showTitles: true),
            bottomTitles: SideTitles(showTitles: true),
          ),
          borderData: FlBorderData(show: false),
          lineBarsData: [
            LineChartBarData(
              spots: [
                FlSpot(0, 3),
                FlSpot(1, 5),
                FlSpot(2, 7),
                FlSpot(3, 10),
                FlSpot(4, 8),
              ],
              isCurved: true,
              colors: [Colors.blue],
              dotData: FlDotData(show: false),
            ),
          ],
        ),
      ),
    );
  }
}

enum UserRole { Admin, Manager, Employee }
