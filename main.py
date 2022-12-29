import hashlib
import os
import sys
import time

import AuthService as Auth


def expect(expected, actual):
    if expected != actual:
        print(f'Expected {expected} but got {actual}')
        sys.exit(1)


def main():
    db = {
        'users': {}
    }

    authService = Auth.AuthService(db)

    # Register test users
    authService.register('test1', 'test1')
    authService.register('test2', 'test2')
    authService.register('test3', 'test3')
    
    # Test login
    expect(True, authService.login('test1', 'test1'))
    expect(True, authService.login('test2', 'test2'))
    expect(True, authService.login('test3', 'test3'))

    # Test login with wrong password
    expect(False, authService.login('test1', 'test2'))
    expect(False, authService.login('test2', 'test1'))
    expect(False, authService.login('test3', 'test1'))

    # Register test user with existing password
    authService.register('test4', 'test1')

    expect(True, authService.login('test4', 'test1'))
    expect(False, authService.login('test4', 'test2'))

    expect(True, authService.login('test1', 'test1'))

    # Change password
    authService.changePassword('test1', 'test1', 'test12')
    expect(False, authService.login('test1', 'test1'))
    expect(True, authService.login('test1', 'test12'))

    # Reset password
    authService.resetPassword('test1', 'test13')
    expect(False, authService.login('test1', 'test12'))
    expect(True, authService.login('test1', 'test13'))

    




    authService.logPasswords()




if __name__ == '__main__':
    main()
