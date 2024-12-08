export const clientRoles = [
  "client",
  "reception",
  "service",
  "cleaning",
  "planning",
  "admin",
] as const;
export type ClientRole = (typeof clientRoles)[number];

export type Client = {
  id: number;
  name: string;
  phone_number: string;
  role: ClientRole;
  picture?: string;
};

export type Room = {
  id: number;
  room_class: number;
};
