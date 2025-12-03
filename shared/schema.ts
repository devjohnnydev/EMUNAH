import { sql } from "drizzle-orm";
import { 
  pgTable, 
  text, 
  varchar, 
  serial, 
  integer, 
  decimal, 
  timestamp, 
  jsonb,
  boolean
} from "drizzle-orm/pg-core";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";
import { z } from "zod";

// Users Table
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  role: text("role").notNull().default("SELLER"), // ADMIN, SELLER, SUPPLIER
  phone: text("phone"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertUserSchema = createInsertSchema(users).omit({ id: true, createdAt: true });
export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// Clients Table
export const clients = pgTable("clients", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  cpfCnpj: text("cpf_cnpj"),
  email: text("email"),
  phone: text("phone"),
  address: text("address"),
  city: text("city"),
  state: text("state"),
  zipCode: text("zip_code"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertClientSchema = createInsertSchema(clients).omit({ id: true, createdAt: true });
export type InsertClient = z.infer<typeof insertClientSchema>;
export type Client = typeof clients.$inferSelect;

// Suppliers Table
export const suppliers = pgTable("suppliers", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  contactName: text("contact_name"),
  cnpj: text("cnpj"),
  email: text("email"),
  phone: text("phone"),
  address: text("address"),
  productionTimeDays: integer("production_time_days").default(7),
  rating: decimal("rating", { precision: 2, scale: 1 }).default("0"),
  paymentMethod: text("payment_method"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertSupplierSchema = createInsertSchema(suppliers).omit({ id: true, createdAt: true });
export type InsertSupplier = z.infer<typeof insertSupplierSchema>;
export type Supplier = typeof suppliers.$inferSelect;

// Products (T-shirts) Table
export const products = pgTable("products", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  model: text("model").notNull(), // basic, polo, oversized
  fabric: text("fabric").notNull(), // cotton, pv, dry-fit
  color: text("color").notNull(),
  sizes: jsonb("sizes").$type<string[]>().notNull(), // ["PP", "P", "M", "G", "GG", "XG"]
  basePrice: decimal("base_price", { precision: 10, scale: 2 }).default("0"),
  stock: integer("stock").default(0),
  imageUrl: text("image_url"),
  active: boolean("active").default(true),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertProductSchema = createInsertSchema(products).omit({ id: true, createdAt: true });
export type InsertProduct = z.infer<typeof insertProductSchema>;
export type Product = typeof products.$inferSelect;

// Prints (Estampas) Table
export const prints = pgTable("prints", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  fileUrl: text("file_url"),
  colors: jsonb("colors").$type<string[]>().notNull(), // ["Preto", "Branco"]
  positions: jsonb("positions").$type<string[]>().notNull(), // ["Peito", "Costas", "Manga"]
  technique: text("technique").default("silk"), // silk, dtf, bordado
  dimensions: text("dimensions"), // "10x10cm"
  active: boolean("active").default(true),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertPrintSchema = createInsertSchema(prints).omit({ id: true, createdAt: true });
export type InsertPrint = z.infer<typeof insertPrintSchema>;
export type Print = typeof prints.$inferSelect;

// Quotes Table
export const quotes = pgTable("quotes", {
  id: serial("id").primaryKey(),
  clientId: integer("client_id").notNull().references(() => clients.id),
  sellerId: integer("seller_id").notNull().references(() => users.id),
  supplierId: integer("supplier_id").references(() => suppliers.id),
  productId: integer("product_id").references(() => products.id),
  printId: integer("print_id").references(() => prints.id),
  items: jsonb("items").$type<{
    productId: number;
    printId?: number;
    sizeGrid: Record<string, number>; // { "P": 10, "M": 20 }
    position?: string;
    technique?: string;
  }[]>().notNull(),
  status: text("status").notNull().default("pending"), // pending, sent, responded, approved, rejected
  totalQuantity: integer("total_quantity").notNull().default(0),
  unitPrice: decimal("unit_price", { precision: 10, scale: 2 }),
  totalPrice: decimal("total_price", { precision: 10, scale: 2 }),
  deliveryDays: integer("delivery_days"),
  supplierResponse: text("supplier_response"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  respondedAt: timestamp("responded_at"),
});

export const insertQuoteSchema = createInsertSchema(quotes).omit({ id: true, createdAt: true, respondedAt: true });
export type InsertQuote = z.infer<typeof insertQuoteSchema>;
export type Quote = typeof quotes.$inferSelect;

// Budgets Table
export const budgets = pgTable("budgets", {
  id: serial("id").primaryKey(),
  quoteId: integer("quote_id").notNull().references(() => quotes.id),
  clientId: integer("client_id").notNull().references(() => clients.id),
  budgetNumber: text("budget_number").notNull().unique(), // ORC-1001
  totalValue: decimal("total_value", { precision: 10, scale: 2 }).notNull(),
  downPaymentPercent: integer("down_payment_percent").default(50),
  downPaymentValue: decimal("down_payment_value", { precision: 10, scale: 2 }).notNull(),
  pixKey: text("pix_key").notNull(),
  status: text("status").notNull().default("draft"), // draft, sent, approved, rejected, cancelled
  validUntil: timestamp("valid_until").notNull(),
  pdfUrl: text("pdf_url"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  sentAt: timestamp("sent_at"),
  approvedAt: timestamp("approved_at"),
});

export const insertBudgetSchema = createInsertSchema(budgets).omit({ id: true, createdAt: true, sentAt: true, approvedAt: true });
export type InsertBudget = z.infer<typeof insertBudgetSchema>;
export type Budget = typeof budgets.$inferSelect;

// Orders Table
export const orders = pgTable("orders", {
  id: serial("id").primaryKey(),
  budgetId: integer("budget_id").notNull().references(() => budgets.id),
  clientId: integer("client_id").notNull().references(() => clients.id),
  supplierId: integer("supplier_id").notNull().references(() => suppliers.id),
  orderNumber: text("order_number").notNull().unique(), // PED-2024-001
  status: text("status").notNull().default("approved"), // approved, production, sent, delivered
  productionStep: text("production_step").default("cutting"), // cutting, printing, sewing, shipping, completed
  progress: integer("progress").default(0), // 0-100
  totalValue: decimal("total_value", { precision: 10, scale: 2 }).notNull(),
  deliveryDate: timestamp("delivery_date"),
  trackingCode: text("tracking_code"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  deliveredAt: timestamp("delivered_at"),
});

export const insertOrderSchema = createInsertSchema(orders).omit({ id: true, createdAt: true, deliveredAt: true });
export type InsertOrder = z.infer<typeof insertOrderSchema>;
export type Order = typeof orders.$inferSelect;

// Transactions Table
export const transactions = pgTable("transactions", {
  id: serial("id").primaryKey(),
  orderId: integer("order_id").notNull().references(() => orders.id),
  paymentMethod: text("payment_method").notNull(), // pix, credit, boleto
  amount: decimal("amount", { precision: 10, scale: 2 }).notNull(),
  status: text("status").notNull().default("pending"), // pending, confirmed, cancelled
  transactionDate: timestamp("transaction_date").defaultNow().notNull(),
  notes: text("notes"),
});

export const insertTransactionSchema = createInsertSchema(transactions).omit({ id: true, transactionDate: true });
export type InsertTransaction = z.infer<typeof insertTransactionSchema>;
export type Transaction = typeof transactions.$inferSelect;
