
export default function Footer() {
  return (
    <>
      <div className="main_footer col-12 col-lg-12 col-md-12 col-sm-12 shadow position-fixed bottom-0 p-2 text-white w-100 m-0">
        <div className="footer_text text-center">
          &copy; {new Date().getFullYear()} Hotel Management Application | Admin
          Panel
        </div>
      </div>
    </>
  );
}
