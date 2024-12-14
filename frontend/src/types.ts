export type Pagination<T> = {
  current_page: number;
  total_pages: number;
  count: number;
  results: T[];
};

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

export type Service = {
  id: number;
  service_description: string;
  service_price: number;
  classes: number[];
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
