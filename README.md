# ts_jupyter

**Калькулятор для тепловых сетей на Jupyter ноутбуках.**

## Установка и настройка

### Создание среды окружения (environment)

1. **Создайте новую среду с нужной версией Python**:

   ```bash
   conda create --name ts_jupyter python=3.13
   ```

2. **Активируйте созданную среду**:

   ```bash
   conda activate ts_jupyter
   ```

3. **Установите необходимые пакеты** (например, pandas):

   ```bash
   conda install pandas
   ```

### Настройка ядра (ipykernel)

1. **Установите ядро IPython**:

   ```bash
   conda install ipykernel
   ```

2. **Просмотрите список доступных ядер**:

   ```bash
   jupyter kernelspec list
   ```

3. **Добавьте ваше ядро в Jupyter**:

   ```bash
   python -m ipykernel install --user --name=ts_jupyter
   ```

4. **Удалите ненужное ядро** (если необходимо):

   ```bash
   jupyter kernelspec uninstall <kernel_name>
   ```

   Замените `<kernel_name>` на имя ядра, которое хотите удалить.

### Экспорт и импорт среды окружения

1. **Экспортируйте все установленные пакеты в файл**:

   ```bash
   conda env export > ts_jupyter.yaml
   ```

2. **Создайте среду из файла**:

   ```bash
   conda env create -f ts_jupyter.yaml
   ```


