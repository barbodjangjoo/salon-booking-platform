# Salon Booking Platform

A production-oriented backend for managing beauty salon services, staff availability, appointments, authentication, and online payments.

Built with Django and PostgreSQL, with a modular architecture designed to support real-world salon booking workflows.

## Overview

Salon Booking Platform provides the backend infrastructure for a beauty salon management and appointment booking system.

The project focuses on solving common problems in appointment-based businesses:

- Managing salon services and categories
- Managing staff and their availability
- Creating and managing appointments
- User authentication with OTP
- Online payment processing
- Separating business domains into maintainable Django applications

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- OTP Authentication
- ZarinPal Payment Gateway

## Architecture

The backend is organized into separate Django applications based on business responsibilities:

```text
backend/
├── config/
├── core/
├── otp/
├── payment/
└── salon/