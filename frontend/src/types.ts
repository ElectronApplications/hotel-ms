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

export type Class = {
  id: number;
  class_description: string;
  place_price: number;
};

export type Room = {
  id: number;
  room_class: number;
};

export const placeStatuses = ["free", "notready", "taken"] as const;
export type PlaceStatus = (typeof placeStatuses)[number];

export type Place = {
  id: number;
  room: number;
  status: PlaceStatus;
};
