function ListGroup() {
  let items = ["New York", "San Francisco", "Tokyo", "London", "Paris"];
  // items = [];
  // const message = items.length === 0 ? <p>No item found</p> : null;
  return (
    <>
      <h1>List Group</h1>
      <ul className="list-group">
        {items.length === 0 ? <p>No item found...!</p> : null}

        {items.map((item) => (
          <li key={item} className="list-group-item">
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
