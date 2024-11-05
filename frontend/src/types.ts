export type Client = {
  id: number;
  name: string;
  phone_number: string;
  role: "client" | "reception" | "service" | "cleaning" | "planning" | "admin";
};
