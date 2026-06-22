from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import jdatetime
from datetime import time, timedelta

from .models import (
    Category, Service, Staff, Availability, Slot, Appointment
)
from core.models import CustomUser


class SalonAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()   # مهم: از APIClient استفاده کن

        # کاربر مشتری
        self.customer = CustomUser.objects.create(
            phone_number='09123456789',
            first_name='مشتری',
            last_name='تست',
        )
        self.customer.set_password('testpass123')
        self.customer.save()

        # کاربر کارمند
        self.staff_user = CustomUser.objects.create(
            phone_number='09129876543',
            first_name='کارمند',
            last_name='تست',
        )
        self.staff_user.set_password('testpass123')
        self.staff_user.save()

        self.category = Category.objects.create(title='مو و زیبایی')
        
        self.service = Service.objects.create(
            category=self.category,
            title='کوتاهی مو',
            duration=60,
            reserve_fee=50000,
        )

        self.staff = Staff.objects.create(user=self.staff_user)
        self.staff.service.add(self.service)

        tomorrow = jdatetime.date.today() + timedelta(days=1)

        self.availability = Availability.objects.create(
            staff=self.staff,
            date=tomorrow,
            start_time=time(9, 0),
            end_time=time(17, 0),
            is_active=True
        )

        self.slot = Slot.objects.create(
            staff=self.staff,
            availability=self.availability,
            date=tomorrow,
            start_time=time(10, 0),
            end_time=time(11, 0),
            status='available'
        )

    # ==================== تست GET ====================

    def test_category_list(self):
        url = reverse('category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_service_list(self):
        url = reverse('service_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_list(self):
        url = reverse('staff_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_slot_list(self):
        url = reverse('slots_list', kwargs={'pk': self.staff.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_list_unauthenticated(self):
        url = reverse('appointment_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================== تست POST ====================

    def test_create_appointment_success(self):
        self.client.force_authenticate(user=self.customer)
        
        url = reverse('appointment_list')
        data = {
            'slot_id': self.slot.pk,
            'service_id': self.service.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.status, 'reserved')

    def test_create_appointment_slot_not_available(self):
        self.client.force_authenticate(user=self.customer)
        
        self.slot.status = 'reserved'
        self.slot.save()
        
        url = reverse('appointment_list')
        data = {
            'slot_id': self.slot.pk,
            'service_id': self.service.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_appointment_wrong_service(self):
        self.client.force_authenticate(user=self.customer)
        
        wrong_service = Service.objects.create(
            category=self.category,
            title='رنگ مو',
            duration=90,
            reserve_fee=100000,
        )
        
        url = reverse('appointment_list')
        data = {
            'slot_id': self.slot.pk,
            'service_id': wrong_service.pk
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==================== سریالایزر ====================

    def test_create_appointment_serializer_valid(self):
        from .serializers import CreateAppointmentSerializer
        data = {'slot_id': self.slot.pk, 'service_id': self.service.pk}
        serializer = CreateAppointmentSerializer(data=data)
        self.assertTrue(serializer.is_valid())