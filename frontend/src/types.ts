export type Client = {
  id: number;
  name: string;
  phone_number: string;
  role: "client" | "reception" | "service" | "cleaning" | "planning" | "admin";
};

export type Room = {
  id: number;
  room_class: number;
};
