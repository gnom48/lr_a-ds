# АиСД

### Запуск тестов из корня: 
```cmd
python -m pytest ./tests/hash_table_tests.py -v
```

### Запуска sandbox из корня:
```cmd
python -m sandbox.main
```

### Запуск бенчмарков из корня
```cmd
python -m pytest .\benchmarks\set_benchmarks.py -v --benchmark-only -p pytest_benchmark
```
