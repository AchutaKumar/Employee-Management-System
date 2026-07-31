from django.test import TestCase, Client
from django.contrib.auth.models import User
from employees.models import Employee
from datetime import date

class UserSessionAndStateManagementTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.emp1 = Employee.objects.create(
            user=self.user1,
            name='Alice Smith',
            email='alice@example.com',
            department='Engineering',
            role='Developer',
            status='Active',
            salary=90000,
            joining_date=date(2023, 1, 1)
        )
        self.emp2 = Employee.objects.create(
            user=self.user2,
            name='Bob Jones',
            email='bob@example.com',
            department='Marketing',
            role='Manager',
            status='Active',
            salary=85000,
            joining_date=date(2023, 2, 1)
        )
        
        self.client1 = Client()
        self.client1.login(username='user1', password='password123')

        self.client2 = Client()
        self.client2.login(username='user2', password='password123')

    def test_user_data_isolation(self):
        """User 1 should only see user 1's employees, not user 2's."""
        response1 = self.client1.get('/')
        self.assertContains(response1, 'Alice Smith')
        self.assertNotContains(response1, 'Bob Jones')

        response2 = self.client2.get('/')
        self.assertContains(response2, 'Bob Jones')
        self.assertNotContains(response2, 'Alice Smith')

    def test_session_state_persistence(self):
        """Filters applied in one request should persist in session for subsequent requests."""
        # User 1 sets department filter
        response = self.client1.get('/?department=Engineering')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client1.session['employee_filters']['department'], 'Engineering')

        # Subsequent GET without query parameters should restore filter from session
        response_restored = self.client1.get('/')
        self.assertEqual(response_restored.context['selected_dept'], 'Engineering')

    def test_session_state_reset(self):
        """Accessing ?reset=true should clear saved filter session state."""
        self.client1.get('/?department=Engineering')
        self.assertIn('employee_filters', self.client1.session)

        response_reset = self.client1.get('/?reset=true', follow=True)
        self.assertNotIn('employee_filters', self.client1.session)

