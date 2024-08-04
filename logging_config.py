dict_config = {
  'version': 1,
  'disable_existing_loggers': False,
  'loggers': {
    'root': {
      'level': 'DEBUG',
      'handlers': [
        'file_handler', 'console_handler'
      ]
    },
    'app': {
      'level': 'INFO',
      'handlers': [
        'file_handler', 'console_handler'
      ],
      'qualname': 'appLogger',
      'propagate': 0
    },
    'storage': {
        'level': 'INFO',
        'handlers': [
          'file_handler', 'console_handler'
        ],
        'qualname': 'appLogger',
        'propagate': 0
      },
    'local': {
        'level': 'INFO',
        'handlers': [
          'file_handler', 'console_handler'
        ],
        'qualname': 'appLogger',
        'propagate': 0
      },
    'config': {
      'level': 'INFO',
      'handlers': [
        'file_handler', 'console_handler'
      ],
      'qualname': 'appLogger',
      'propagate': 0
    }
  },
  'formatters': {
    'base': {
      'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s',
      'datefmt': '%Y-%m-%dT%H:%M:%S%Z'
    }
  },
  'handlers': {
    'console_handler': {
      'class': 'logging.StreamHandler',
      'level': 'INFO',
      'formatter': 'base'
    },
    'file_handler': {
      'class': 'logging.FileHandler',
      'level': 'DEBUG',
      'formatter': 'base',
      'filename': 'logfile.log'
    }
  }
}
