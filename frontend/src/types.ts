export type Pagination<T> = {
  current_page: number;
  total_pages: number;
  count: number;
  results: T[];
};

export type Gallery = {
  id: number;
  name: string;
  images: {
    id: number;
    image: string;
  }[];
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
  picture: string | null;
};

export type Class = {
  id: number;
  class_description: string;
  place_price: number;
  gallery: Gallery | null;
};

export type Service = {
  id: number;
  service_description: string;
  service_price: number;
  classes: number[];
  gallery: Gallery | null;
};

export const roomStatuses = ["free", "notready", "taken"] as const;
export type RoomStatus = (typeof roomStatuses)[number];

export type Room = {
  id: number;
  room_number: number;
  room_class: number;
  status: RoomStatus;
  places: number;
};

export type Accomodation = {
  id: number;
  room: Room;
  move_in_time: string;
  move_out_time: string;
  client: Client;
  price_to_pay: number;
  was_price_paid: boolean;
  checked_out: boolean;
  reservation: number | null;
};
