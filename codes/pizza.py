from abc import ABC, abstractmethod
from enum import Enum

class PizzaSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

# Pizza 接口
class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

# BasePizza 类实现 Pizza 接口
class BasePizza(Pizza):
    def __init__(self, size: PizzaSize):
        self.size = size
    
    def get_description(self) -> str:
        return f"{self.size.value.capitalize()} pizza"
    
    def get_cost(self) -> float:
        # 根据尺寸设置基础价格
        size_prices = {
            PizzaSize.SMALL: 8.0,
            PizzaSize.MEDIUM: 12.0,
            PizzaSize.LARGE: 16.0
        }
        return size_prices[self.size]

# PizzaDecorator 装饰器基类
class PizzaDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza
    
    def get_description(self) -> str:
        return self.pizza.get_description()
    
    def get_cost(self) -> float:
        return self.pizza.get_cost()

# 具体的 Topping 装饰器
class CheeseTopping(PizzaDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
    
    def get_description(self) -> str:
        return self.pizza.get_description() + " + Cheese"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 2.0

class PepperoniTopping(PizzaDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
    
    def get_description(self) -> str:
        return self.pizza.get_description() + " + Pepperoni"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 3.0

class MushroomTopping(PizzaDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
    
    def get_description(self) -> str:
        return self.pizza.get_description() + " + Mushroom"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.5

class OliveTopping(PizzaDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
    
    def get_description(self) -> str:
        return self.pizza.get_description() + " + Olive"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.0

class TomatoTopping(PizzaDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
    
    def get_description(self) -> str:
        return self.pizza.get_description() + " + Tomato"
    
    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.0

# 示例使用
if __name__ == "__main__":
    # 创建一个中号 pizza
    pizza = BasePizza(PizzaSize.MEDIUM)
    print(f"Base pizza: {pizza.get_description()}, Cost: ${pizza.get_cost()}")
    
    # 添加奶酪
    pizza = CheeseTopping(pizza)
    print(f"After adding cheese: {pizza.get_description()}, Cost: ${pizza.get_cost()}")
    
    # 添加意大利辣肠
    pizza = PepperoniTopping(pizza)
    print(f"After adding pepperoni: {pizza.get_description()}, Cost: ${pizza.get_cost()}")
    
    # 添加蘑菇
    pizza = MushroomTopping(pizza)
    print(f"After adding mushroom: {pizza.get_description()}, Cost: ${pizza.get_cost()}")
    
    # 添加橄榄
    pizza = OliveTopping(pizza)
    print(f"After adding olive: {pizza.get_description()}, Cost: ${pizza.get_cost()}")
    
    print("\n" + "="*50 + "\n")
    
    # 创建另一个大号 pizza 的例子
    large_pizza = BasePizza(PizzaSize.LARGE)
    large_pizza = CheeseTopping(large_pizza)
    large_pizza = TomatoTopping(large_pizza)
    large_pizza = MushroomTopping(large_pizza)
    
    print(f"Large pizza example: {large_pizza.get_description()}")
    print(f"Total cost: ${large_pizza.get_cost()}")