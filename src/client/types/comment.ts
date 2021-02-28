export interface Comment {
  id: string;
  author: string;
  body: string;
  object: string;
  created_date: Date;
}

export function isComment(data: any): data is Comment {
  return (
    data &&
    data.id &&
    data.author &&
    data.body &&
    data.object &&
    data.created_date
  );
}
