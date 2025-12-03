import { db } from "./db";
import { 
  users, 
  clients, 
  suppliers, 
  products, 
  prints, 
  quotes, 
  budgets, 
  orders, 
  transactions,
  type InsertUser,
  type User,
  type InsertClient,
  type Client,
  type InsertSupplier,
  type Supplier,
  type InsertProduct,
  type Product,
  type InsertPrint,
  type Print,
  type InsertQuote,
  type Quote,
  type InsertBudget,
  type Budget,
  type InsertOrder,
  type Order,
  type InsertTransaction,
  type Transaction
} from "@shared/schema";
import { eq, desc, and, sql } from "drizzle-orm";

export interface IStorage {
  // Users
  getUser(id: number): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // Clients
  getClients(): Promise<Client[]>;
  getClient(id: number): Promise<Client | undefined>;
  createClient(client: InsertClient): Promise<Client>;
  updateClient(id: number, client: Partial<InsertClient>): Promise<Client | undefined>;
  deleteClient(id: number): Promise<void>;

  // Suppliers
  getSuppliers(): Promise<Supplier[]>;
  getSupplier(id: number): Promise<Supplier | undefined>;
  createSupplier(supplier: InsertSupplier): Promise<Supplier>;
  updateSupplier(id: number, supplier: Partial<InsertSupplier>): Promise<Supplier | undefined>;
  deleteSupplier(id: number): Promise<void>;

  // Products
  getProducts(): Promise<Product[]>;
  getProduct(id: number): Promise<Product | undefined>;
  createProduct(product: InsertProduct): Promise<Product>;
  updateProduct(id: number, product: Partial<InsertProduct>): Promise<Product | undefined>;
  deleteProduct(id: number): Promise<void>;

  // Prints
  getPrints(): Promise<Print[]>;
  getPrint(id: number): Promise<Print | undefined>;
  createPrint(print: InsertPrint): Promise<Print>;
  updatePrint(id: number, print: Partial<InsertPrint>): Promise<Print | undefined>;
  deletePrint(id: number): Promise<void>;

  // Quotes
  getQuotes(): Promise<Quote[]>;
  getQuote(id: number): Promise<Quote | undefined>;
  createQuote(quote: InsertQuote): Promise<Quote>;
  updateQuote(id: number, quote: Partial<InsertQuote>): Promise<Quote | undefined>;
  deleteQuote(id: number): Promise<void>;

  // Budgets
  getBudgets(): Promise<Budget[]>;
  getBudget(id: number): Promise<Budget | undefined>;
  createBudget(budget: InsertBudget): Promise<Budget>;
  updateBudget(id: number, budget: Partial<InsertBudget>): Promise<Budget | undefined>;
  deleteBudget(id: number): Promise<void>;

  // Orders
  getOrders(): Promise<Order[]>;
  getOrder(id: number): Promise<Order | undefined>;
  createOrder(order: InsertOrder): Promise<Order>;
  updateOrder(id: number, order: Partial<InsertOrder>): Promise<Order | undefined>;
  deleteOrder(id: number): Promise<void>;

  // Transactions
  getTransactions(orderId: number): Promise<Transaction[]>;
  createTransaction(transaction: InsertTransaction): Promise<Transaction>;

  // Dashboard Metrics
  getDashboardMetrics(): Promise<{
    totalRevenue: number;
    completedOrders: number;
    pendingBudgets: number;
    averageTicket: number;
  }>;
}

export class DatabaseStorage implements IStorage {
  // Users
  async getUser(id: number): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id)).limit(1);
    return user;
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.email, email)).limit(1);
    return user;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const [user] = await db.insert(users).values(insertUser).returning();
    return user;
  }

  // Clients
  async getClients(): Promise<Client[]> {
    return await db.select().from(clients).orderBy(desc(clients.createdAt));
  }

  async getClient(id: number): Promise<Client | undefined> {
    const [client] = await db.select().from(clients).where(eq(clients.id, id)).limit(1);
    return client;
  }

  async createClient(client: InsertClient): Promise<Client> {
    const [newClient] = await db.insert(clients).values(client).returning();
    return newClient;
  }

  async updateClient(id: number, client: Partial<InsertClient>): Promise<Client | undefined> {
    const [updated] = await db.update(clients).set(client).where(eq(clients.id, id)).returning();
    return updated;
  }

  async deleteClient(id: number): Promise<void> {
    await db.delete(clients).where(eq(clients.id, id));
  }

  // Suppliers
  async getSuppliers(): Promise<Supplier[]> {
    return await db.select().from(suppliers).orderBy(desc(suppliers.createdAt));
  }

  async getSupplier(id: number): Promise<Supplier | undefined> {
    const [supplier] = await db.select().from(suppliers).where(eq(suppliers.id, id)).limit(1);
    return supplier;
  }

  async createSupplier(supplier: InsertSupplier): Promise<Supplier> {
    const [newSupplier] = await db.insert(suppliers).values(supplier).returning();
    return newSupplier;
  }

  async updateSupplier(id: number, supplier: Partial<InsertSupplier>): Promise<Supplier | undefined> {
    const [updated] = await db.update(suppliers).set(supplier).where(eq(suppliers.id, id)).returning();
    return updated;
  }

  async deleteSupplier(id: number): Promise<void> {
    await db.delete(suppliers).where(eq(suppliers.id, id));
  }

  // Products
  async getProducts(): Promise<Product[]> {
    return await db.select().from(products).orderBy(desc(products.createdAt));
  }

  async getProduct(id: number): Promise<Product | undefined> {
    const [product] = await db.select().from(products).where(eq(products.id, id)).limit(1);
    return product;
  }

  async createProduct(product: InsertProduct): Promise<Product> {
    const [newProduct] = await db.insert(products).values(product).returning();
    return newProduct;
  }

  async updateProduct(id: number, product: Partial<InsertProduct>): Promise<Product | undefined> {
    const [updated] = await db.update(products).set(product).where(eq(products.id, id)).returning();
    return updated;
  }

  async deleteProduct(id: number): Promise<void> {
    await db.delete(products).where(eq(products.id, id));
  }

  // Prints
  async getPrints(): Promise<Print[]> {
    return await db.select().from(prints).orderBy(desc(prints.createdAt));
  }

  async getPrint(id: number): Promise<Print | undefined> {
    const [print] = await db.select().from(prints).where(eq(prints.id, id)).limit(1);
    return print;
  }

  async createPrint(print: InsertPrint): Promise<Print> {
    const [newPrint] = await db.insert(prints).values(print).returning();
    return newPrint;
  }

  async updatePrint(id: number, print: Partial<InsertPrint>): Promise<Print | undefined> {
    const [updated] = await db.update(prints).set(print).where(eq(prints.id, id)).returning();
    return updated;
  }

  async deletePrint(id: number): Promise<void> {
    await db.delete(prints).where(eq(prints.id, id));
  }

  // Quotes
  async getQuotes(): Promise<Quote[]> {
    return await db.select().from(quotes).orderBy(desc(quotes.createdAt));
  }

  async getQuote(id: number): Promise<Quote | undefined> {
    const [quote] = await db.select().from(quotes).where(eq(quotes.id, id)).limit(1);
    return quote;
  }

  async createQuote(quote: InsertQuote): Promise<Quote> {
    const [newQuote] = await db.insert(quotes).values(quote).returning();
    return newQuote;
  }

  async updateQuote(id: number, quote: Partial<InsertQuote>): Promise<Quote | undefined> {
    const [updated] = await db.update(quotes).set(quote).where(eq(quotes.id, id)).returning();
    return updated;
  }

  async deleteQuote(id: number): Promise<void> {
    await db.delete(quotes).where(eq(quotes.id, id));
  }

  // Budgets
  async getBudgets(): Promise<Budget[]> {
    return await db.select().from(budgets).orderBy(desc(budgets.createdAt));
  }

  async getBudget(id: number): Promise<Budget | undefined> {
    const [budget] = await db.select().from(budgets).where(eq(budgets.id, id)).limit(1);
    return budget;
  }

  async createBudget(budget: InsertBudget): Promise<Budget> {
    const [newBudget] = await db.insert(budgets).values(budget).returning();
    return newBudget;
  }

  async updateBudget(id: number, budget: Partial<InsertBudget>): Promise<Budget | undefined> {
    const [updated] = await db.update(budgets).set(budget).where(eq(budgets.id, id)).returning();
    return updated;
  }

  async deleteBudget(id: number): Promise<void> {
    await db.delete(budgets).where(eq(budgets.id, id));
  }

  // Orders
  async getOrders(): Promise<Order[]> {
    return await db.select().from(orders).orderBy(desc(orders.createdAt));
  }

  async getOrder(id: number): Promise<Order | undefined> {
    const [order] = await db.select().from(orders).where(eq(orders.id, id)).limit(1);
    return order;
  }

  async createOrder(order: InsertOrder): Promise<Order> {
    const [newOrder] = await db.insert(orders).values(order).returning();
    return newOrder;
  }

  async updateOrder(id: number, order: Partial<InsertOrder>): Promise<Order | undefined> {
    const [updated] = await db.update(orders).set(order).where(eq(orders.id, id)).returning();
    return updated;
  }

  async deleteOrder(id: number): Promise<void> {
    await db.delete(orders).where(eq(orders.id, id));
  }

  // Transactions
  async getTransactions(orderId: number): Promise<Transaction[]> {
    return await db.select().from(transactions).where(eq(transactions.orderId, orderId));
  }

  async createTransaction(transaction: InsertTransaction): Promise<Transaction> {
    const [newTransaction] = await db.insert(transactions).values(transaction).returning();
    return newTransaction;
  }

  // Dashboard Metrics
  async getDashboardMetrics() {
    const [revenueResult] = await db
      .select({ total: sql<number>`COALESCE(SUM(${orders.totalValue}::numeric), 0)` })
      .from(orders)
      .where(eq(orders.status, "delivered"));

    const [ordersResult] = await db
      .select({ count: sql<number>`COUNT(*)` })
      .from(orders)
      .where(eq(orders.status, "delivered"));

    const [budgetsResult] = await db
      .select({ count: sql<number>`COUNT(*)` })
      .from(budgets)
      .where(eq(budgets.status, "sent"));

    const [avgResult] = await db
      .select({ avg: sql<number>`COALESCE(AVG(${orders.totalValue}::numeric), 0)` })
      .from(orders)
      .where(eq(orders.status, "delivered"));

    return {
      totalRevenue: Number(revenueResult.total) || 0,
      completedOrders: Number(ordersResult.count) || 0,
      pendingBudgets: Number(budgetsResult.count) || 0,
      averageTicket: Number(avgResult.avg) || 0,
    };
  }
}

export const storage = new DatabaseStorage();
