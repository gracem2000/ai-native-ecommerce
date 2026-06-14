"""
商品匹配模块
基于场景关键词自动关联商品库
"""
import json
from typing import List, Dict, Optional
from src.config import Config


class ProductMatching:
    """商品匹配类 - 基于场景关键词匹配商品"""

    def __init__(self):
        """初始化商品匹配器"""
        self.products = []
        self._load_products()

    def _load_products(self):
        """加载商品库"""
        try:
            with open(Config.PRODUCT_DB_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.products = data.get('products', [])
                print(f"📦 已加载 {len(self.products)} 个商品")
        except FileNotFoundError:
            print(f"⚠️  商品库文件不存在: {Config.PRODUCT_DB_PATH}")
            print(f"   请创建商品库文件或运行初始化脚本")
            self.products = []
        except Exception as e:
            print(f"⚠️  加载商品库失败: {e}")
            self.products = []

    def match_products(
        self,
        keywords: List[str],
        top_k: Optional[int] = None,
        group_by_category: bool = True
    ) -> List[Dict]:
        """基于关键词匹配商品

        Args:
            keywords: 场景关键词列表
            top_k: 返回商品数量，默认使用配置值
            group_by_category: 是否按品类分组

        Returns:
            匹配的商品列表，按相关性排序（如启用分组则返回品类分组结构）
        """
        if top_k is None:
            top_k = Config.MAX_MATCH_PRODUCTS

        if not self.products:
            print("⚠️  商品库为空，无法进行匹配")
            return []

        if not keywords:
            print("⚠️  关键词为空，无法进行匹配")
            return []

        scored_products = []

        for product in self.products:
            score = self._calculate_relevance(product, keywords)
            if score >= Config.MIN_CONFIDENCE:
                scored_products.append({
                    **product,
                    'relevance_score': round(score, 3)
                })

        # 按相关性排序
        scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)

        if group_by_category:
            # 按品类分组
            result = self._group_products_by_category(scored_products[:top_k])
            print(f"   🎯 匹配到 {len(scored_products[:top_k])} 个商品，分为 {len(result)} 个品类")
        else:
            result = scored_products[:top_k]
            print(f"   🎯 匹配到 {len(result)} 个商品 (关键词: {', '.join(keywords[:3])}...)")

        return result

    def _group_products_by_category(self, products: List[Dict]) -> List[Dict]:
        """将商品按品类分组

        Args:
            products: 商品列表

        Returns:
            按品类分组的商品列表
        """
        category_groups = {}

        for product in products:
            category = product.get('category', '未分类')
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(product)

        # 转换为结构化格式
        result = []
        for category, category_products in sorted(category_groups.items()):
            result.append({
                'category': category,
                'product_count': len(category_products),
                'products': category_products
            })

        # 按商品数量排序（商品数多的品类排前面）
        result.sort(key=lambda x: x['product_count'], reverse=True)

        return result

    def _calculate_relevance(self, product: Dict, keywords: List[str]) -> float:
        """
        计算商品与关键词的相关性分数

        策略:
        1. 标题完全匹配: 1.0 分
        2. 标签匹配: 0.8 分
        3. 类别匹配: 0.5 分

        Args:
            product: 商品信息
            keywords: 关键词列表

        Returns:
            相关性分数 (0-1)
        """
        score = 0.0

        for keyword in keywords:
            keyword = keyword.lower().strip()

            # 标题匹配（最高权重）
            if keyword in product.get('title', '').lower():
                score += 1.0

            # 标签匹配
            for tag in product.get('tags', []):
                if keyword in tag.lower():
                    score += 0.8
                    break  # 每个标签只计算一次

            # 类别匹配
            if keyword in product.get('category', '').lower():
                score += 0.5

        return min(score / len(keywords), 1.0)  # 归一化到0-1

    def get_product_by_sku(self, sku_id: str) -> Optional[Dict]:
        """根据SKU ID获取商品

        Args:
            sku_id: 商品SKU ID

        Returns:
            商品信息，不存在返回None
        """
        for product in self.products:
            if product.get('sku_id') == sku_id:
                return product
        return None

    def search_products(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """搜索商品

        Args:
            query: 搜索关键词
            limit: 返回数量

        Returns:
            匹配的商品列表
        """
        query = query.lower()
        results = []

        for product in self.products:
            # 在标题、类别、标签中搜索
            if (query in product.get('title', '').lower() or
                query in product.get('category', '').lower() or
                any(query in tag.lower() for tag in product.get('tags', []))):
                results.append(product)

            if len(results) >= limit:
                break

        return results

    def get_categories(self) -> List[str]:
        """获取所有商品类别

        Returns:
            类别列表
        """
        categories = set()
        for product in self.products:
            categories.add(product.get('category', '未分类'))
        return sorted(list(categories))

    def get_stats(self) -> Dict:
        """获取商品库统计信息

        Returns:
            统计信息字典
        """
        category_count = {}
        for product in self.products:
            category = product.get('category', '未分类')
            category_count[category] = category_count.get(category, 0) + 1

        return {
            'total_products': len(self.products),
            'categories': len(category_count),
            'category_distribution': category_count
        }


if __name__ == "__main__":
    # 测试代码
    matching = ProductMatching()

    # 测试匹配
    test_keywords = ["啤酒", "薯片", "世界杯"]
    results = matching.match_products(test_keywords)

    print("\n=== 匹配结果 ===")
    for product in results:
        print(f"\n📦 {product['title']}")
        print(f"   类别: {product['category']}")
        print(f"   价格: ¥{product['price']}")
        print(f"   相关性: {product['relevance_score']}")

    # 显示统计
    stats = matching.get_stats()
    print(f"\n=== 商品库统计 ===")
    print(f"总商品数: {stats['total_products']}")
    print(f"类别数: {stats['categories']}")
    print(f"类别分布: {stats['category_distribution']}")
