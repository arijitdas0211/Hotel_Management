--
-- Create model Customer
--
CREATE TABLE `customer` (`customer_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `phone` varchar(10) NOT NULL UNIQUE, `email` varchar(100) NOT NULL UNIQUE, `username` varchar(30) NOT NULL UNIQUE, `password` varchar(30) NOT NULL, `address` varchar(200) NOT NULL, `food_pref` integer NOT NULL, `created_at` datetime(6) NOT NULL, `last_login` datetime(6) NOT NULL);
--
-- Create model FoodCategory
--
CREATE TABLE `food_category` (`category_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `category_name` varchar(100) NOT NULL, `food_type` integer NOT NULL, `created_at` datetime(6) NOT NULL, `modified_at` datetime(6) NOT NULL);
--
-- Create model Staff
--
CREATE TABLE `staff` (`staff_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `phone` varchar(10) NOT NULL UNIQUE, `email` varchar(100) NOT NULL UNIQUE, `username` varchar(30) NOT NULL UNIQUE, `password` varchar(30) NOT NULL, `is_active` bool NOT NULL, `is_superuser` bool NOT NULL, `created_at` datetime(6) NOT NULL, `last_login` datetime(6) NOT NULL);
--
-- Create model StaffType
--
CREATE TABLE `staff_type` (`staff_type_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `staff_type_name` varchar(100) NOT NULL);
--
-- Create model SuperUser
--
CREATE TABLE `superuser` (`admin_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `phone` varchar(10) NOT NULL UNIQUE, `email` varchar(100) NOT NULL UNIQUE, `username` varchar(30) NOT NULL UNIQUE, `password` varchar(30) NOT NULL, `is_active` bool NOT NULL, `is_superuser` bool NOT NULL, `created_at` datetime(6) NOT NULL, `last_login` datetime(6) NOT NULL);
--
-- Create model Booking
--
CREATE TABLE `booking` (`booking_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `booking_date` date NOT NULL, `booking_time` time(6) NOT NULL, `no_of_people` integer UNSIGNED NOT NULL CHECK (`no_of_people` >= 0), `booking_status` bool NOT NULL, `customer_id` integer NOT NULL, `staff_id` integer NOT NULL);
--
-- Create model Menu
--
CREATE TABLE `menu` (`menu_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `item_name` varchar(100) NOT NULL, `item_price` double precision NOT NULL, `food_type` integer NOT NULL, `item_status` bool NOT NULL, `item_image` varchar(100) NULL, `created_at` datetime(6) NOT NULL, `modified_at` datetime(6) NOT NULL, `food_category_id` integer NOT NULL, `created_by_id` integer NOT NULL);
--
-- Create model Order
--
CREATE TABLE `order` (`order_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_date` date NOT NULL, `order_time` time(6) NOT NULL, `order_status` bool NOT NULL, `customer_id` integer NOT NULL, `staff_id` integer NOT NULL);
CREATE TABLE `order_items` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `order_id` integer NOT NULL, `menu_id` integer NOT NULL);
--
-- Create model Billing
--
CREATE TABLE `billing` (`bill_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `total_amount` double precision NOT NULL, `bill_date` date NOT NULL, `bill_time` time(6) NOT NULL, `bill_status` bool NOT NULL, `bill_payment_status` bool NOT NULL, `booking_id` integer NOT NULL, `customer_id` integer NOT NULL, `order_id` integer NOT NULL, `staff_id` integer NOT NULL);
--
-- Add field staff_type to staff
--
ALTER TABLE `staff` ADD COLUMN `staff_type_id` integer NOT NULL , ADD CONSTRAINT `staff_staff_type_id_8a3776c2_fk_staff_type_staff_type_id` FOREIGN KEY (`staff_type_id`) REFERENCES `staff_type`(`staff_type_id`);
--
-- Add field created_by to stafftype
--
ALTER TABLE `staff_type` ADD COLUMN `created_by_id` integer NOT NULL , ADD CONSTRAINT `staff_type_created_by_id_349fa277_fk_superuser_admin_id` FOREIGN KEY (`created_by_id`) REFERENCES `superuser`(`admin_id`);
--
-- Add field superuser to staff
--
ALTER TABLE `staff` ADD COLUMN `superuser_id` integer NOT NULL , ADD CONSTRAINT `staff_superuser_id_5fc07978_fk_superuser_admin_id` FOREIGN KEY (`superuser_id`) REFERENCES `superuser`(`admin_id`);
--
-- Create model Table
--
CREATE TABLE `table` (`table_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `table_no` integer NOT NULL UNIQUE, `capacity` integer NOT NULL, `status` bool NOT NULL, `created_at` datetime(6) NOT NULL, `modified_at` datetime(6) NOT NULL, `created_by_id` integer NOT NULL);
--
-- Add field table to order
--
ALTER TABLE `order` ADD COLUMN `table_id` integer NOT NULL , ADD CONSTRAINT `order_table_id_09358604_fk_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `table`(`table_id`);
--
-- Create model Feedback
--
CREATE TABLE `feedback` (`feedback_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `rating` integer NOT NULL, `feedback` longtext NOT NULL, `feedback_date` date NOT NULL, `feedback_time` time(6) NOT NULL, `feedback_status` bool NOT NULL, `billing_id` integer NOT NULL, `customer_id` integer NOT NULL, `staff_id` integer NOT NULL, `table_id` integer NOT NULL);
--
-- Add field table to booking
--
ALTER TABLE `booking` ADD COLUMN `table_id` integer NOT NULL , ADD CONSTRAINT `booking_table_id_a17e8902_fk_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `table`(`table_id`);
--
-- Add field table to billing
--
ALTER TABLE `billing` ADD COLUMN `table_id` integer NOT NULL , ADD CONSTRAINT `billing_table_id_1be0f0b8_fk_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `table`(`table_id`);
ALTER TABLE `booking` ADD CONSTRAINT `booking_customer_id_6791ff7a_fk_customer_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);
ALTER TABLE `booking` ADD CONSTRAINT `booking_staff_id_37421187_fk_staff_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `menu` ADD CONSTRAINT `menu_food_category_id_e8fcee62_fk_food_category_category_id` FOREIGN KEY (`food_category_id`) REFERENCES `food_category` (`category_id`);
ALTER TABLE `menu` ADD CONSTRAINT `menu_created_by_id_5ae9ecd0_fk_staff_staff_id` FOREIGN KEY (`created_by_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `order` ADD CONSTRAINT `order_customer_id_9da9253f_fk_customer_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);
ALTER TABLE `order` ADD CONSTRAINT `order_staff_id_a1cb59f3_fk_staff_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `order_items` ADD CONSTRAINT `order_items_order_id_menu_id_9d9c3b0e_uniq` UNIQUE (`order_id`, `menu_id`);
ALTER TABLE `order_items` ADD CONSTRAINT `order_items_order_id_412ad78b_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`);
ALTER TABLE `order_items` ADD CONSTRAINT `order_items_menu_id_fddd310f_fk_menu_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`);
ALTER TABLE `billing` ADD CONSTRAINT `billing_booking_id_ec2273cf_fk_booking_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`);
ALTER TABLE `billing` ADD CONSTRAINT `billing_customer_id_e385dcd5_fk_customer_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);
ALTER TABLE `billing` ADD CONSTRAINT `billing_order_id_60886b31_fk_order_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`);
ALTER TABLE `billing` ADD CONSTRAINT `billing_staff_id_8f61e980_fk_staff_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `table` ADD CONSTRAINT `table_created_by_id_64e06b04_fk_staff_staff_id` FOREIGN KEY (`created_by_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `feedback` ADD CONSTRAINT `feedback_billing_id_49336aec_fk_billing_bill_id` FOREIGN KEY (`billing_id`) REFERENCES `billing` (`bill_id`);
ALTER TABLE `feedback` ADD CONSTRAINT `feedback_customer_id_a1653a67_fk_customer_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);
ALTER TABLE `feedback` ADD CONSTRAINT `feedback_staff_id_2ad70430_fk_staff_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`staff_id`);
ALTER TABLE `feedback` ADD CONSTRAINT `feedback_table_id_c9d22840_fk_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `table` (`table_id`);
