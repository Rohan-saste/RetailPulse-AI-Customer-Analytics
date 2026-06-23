import React from 'react';

const products = [
  { id: 1, name: 'Wireless Noise-Cancelling Headphones', revenue: '£12,450', orders: 145, growth: '+12%', isPositive: true },
  { id: 2, name: 'Smart Home Hub v2', revenue: '£9,800', orders: 98, growth: '+8%', isPositive: true },
  { id: 3, name: 'Ergonomic Office Chair', revenue: '£7,200', orders: 60, growth: '-3%', isPositive: false },
  { id: 4, name: '4K Ultra HD Monitor', revenue: '£15,600', orders: 42, growth: '+15%', isPositive: true },
  { id: 5, name: 'Mechanical Keyboard (Blue Switch)', revenue: '£4,100', orders: 120, growth: '+5%', isPositive: true },
];

const ProductTable = () => {
  return (
    <div className="bg-card border border-borderLine rounded-2xl shadow-sm h-[450px] flex flex-col overflow-hidden">
      <div className="p-6 border-b border-borderLine">
        <h3 className="text-textMain font-bold text-lg">Top Products</h3>
      </div>
      <div className="flex-1 overflow-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-background text-textMuted text-xs uppercase tracking-wider">
              <th className="p-4 font-semibold">Product</th>
              <th className="p-4 font-semibold">Revenue</th>
              <th className="p-4 font-semibold">Orders</th>
              <th className="p-4 font-semibold">Growth</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-borderLine">
            {products.map((product) => (
              <tr key={product.id} className="hover:bg-background/50 transition-colors">
                <td className="p-4 text-sm font-medium text-textMain">{product.name}</td>
                <td className="p-4 text-sm text-textMain">{product.revenue}</td>
                <td className="p-4 text-sm text-textMain">{product.orders}</td>
                <td className="p-4 text-sm font-medium">
                  <span className={`px-2.5 py-1 rounded-full text-xs ${product.isPositive ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
                    {product.growth}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ProductTable;
